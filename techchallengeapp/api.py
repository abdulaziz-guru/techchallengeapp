"""
This module contains frappe whitelist methods.
"""

import frappe


@frappe.whitelist()
def get_fields(doctype: str) -> list[dict]:
    fields = frappe.get_meta(doctype).as_dict()["fields"]
    # Handle Table Fields
    for field in fields:
        if field["fieldtype"] == "Table":
            field["fields"] = get_fields(field["options"])
    return fields
