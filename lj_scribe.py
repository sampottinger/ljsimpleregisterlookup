import collections

import flask

import ljmmm

TARGET_DEVICE = "T7"


UnresolvedToResolvedPair = collections.namedtuple(
    "UnresolvedToResolvedPair",
    ["unresolved", "resolved"]
)


UnresolvedWithResolvedGrouping = collections.namedtuple(
    "UnresolvedWithResolvedGrouping",
    ["resolved", "unresolved"]
)

REGISTERS_STR_START = "@registers:"
SUBTAG_TEMPLATE_STR = "%s#(%d:%d:%d)%s"
SUBTAG_TEMPLATE_STR_DEFAULT_GAP = "%s#(%d:%d)%s"


def parsed_sub_tag_to_names(entry):
    if not entry.includes_ljmmm:
        return [entry.prefix]

    if entry.num_between_regs: num_between_regs = entry.num_between_regs
    else: num_between_regs = 1

    enumeration_src = (
        entry.prefix,
        entry.start_num,
        entry.start_num + num_between_regs * (entry.num_regs-1),
        entry.num_between_regs,
        entry.postfix
    )
    return ljmmm.generate_int_enumeration(enumeration_src)


def parsed_tag_to_names(tag_entries):
    return map(parsed_sub_tag_to_names, tag_entries)


def get_unres_reg_names_by_subtag_name(tag_names, unres_regs_by_res_name):
    return map(
        lambda x: (x, unres_regs_by_res_name[x]),
        tag_names
    )


def get_unres_reg_names_for_tag_names(tag, unres_regs_by_res_name):
    return map(
        lambda x: get_unres_reg_names_by_subtag_name(x, unres_regs_by_res_name),
        tag
    )


def resolve_registers_by_name_in_tuple(target_tuple, res_regs_by_res_name):
    return map(
        lambda x: (res_regs_by_res_name[x[0]], x[1]),
        target_tuple
    )


def resolve_registers_by_name_in_tag(target_tag, res_regs_by_res_name):
    return map(
        lambda x: resolve_registers_by_name_in_tuple(x, res_regs_by_res_name),
        target_tag
    )


def convert_unresolved_to_resolved_tuple(target_tuple):
    return map(
        lambda x: UnresolvedToResolvedPair(x[1], x[0]),
        target_tuple
    )


def convert_unresolved_to_resolved_tag(target_tag):
    return map(
        convert_unresolved_to_resolved_tuple,
        target_tag
    )


def find_classes(tag_entries, dev_regs):
    regs_tuple_res_name_first = map(lambda x: (x[1]["name"], x[0]), dev_regs)
    unres_regs_by_res_name = dict(regs_tuple_res_name_first)
    res_regs_by_res_name = dict(
        map(lambda x: (x[1]["name"], x[1]), dev_regs)
    )

    tag_names = map(parsed_tag_to_names, tag_entries)
    res_name_to_unres_entry_tuple = map(
        lambda x: get_unres_reg_names_for_tag_names(x, unres_regs_by_res_name),
        tag_names
    )

    res_entry_to_unres_entry_tuple = map(
        lambda x: resolve_registers_by_name_in_tag(x, res_regs_by_res_name),
        res_name_to_unres_entry_tuple
    )

    return map(
        convert_unresolved_to_resolved_tag,
        res_entry_to_unres_entry_tuple
    )


def find_subtags_by_class(unresolved_resolved_pairs, dev_regs):
    ret_dict = collections.OrderedDict()

    unres_regs_by_unres_name = dict(
        map(lambda x: (x[0]["name"], x[0]), dev_regs)
    )

    for entry in unresolved_resolved_pairs:
        unresolved = entry[0].unresolved
        name = unresolved["name"]
        grouping = UnresolvedWithResolvedGrouping(
            map(lambda x: x.resolved, entry), unresolved)
        ret_dict[name] = grouping

    return ret_dict


def organize_tag_by_class(target_tag, dev_regs):
    return map(
        lambda x: find_subtags_by_class(x, dev_regs),
        target_tag
    )


def render_tag_summary(subtag_by_class, orig_tags, orig_tag_str):
    return flask.render_template(
        "tag_summary_template.html",
        tag=zip(orig_tags, subtag_by_class.values()),
        orig_str=orig_tag_str
    )


def find_original_tag_str(parsed_tag):

    REGISTERS_STR_START
    tag_strs = []

    for sub_tag in parsed_tag:
        if not sub_tag.includes_ljmmm:
            tag_strs.append(sub_tag.prefix)
        elif sub_tag.num_between_regs:
            template_values = (
                sub_tag.prefix,
                sub_tag.start_num,
                sub_tag.num_regs,
                sub_tag.num_between_regs,
                sub_tag.postfix
            )
            tag_strs.append(SUBTAG_TEMPLATE_STR % template_values)
        else:
            template_values = (
                sub_tag.prefix,
                sub_tag.start_num,
                sub_tag.num_regs,
                sub_tag.postfix
            )
            tag_strs.append(SUBTAG_TEMPLATE_STR_DEFAULT_GAP % template_values)

    return REGISTERS_STR_START + ",".join(tag_strs)
