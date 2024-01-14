"""
This file contains all the endpoints for the TechChallengeApp
"""

import frappe


@frappe.whitelist(allow_guest=True, methods="POST")
def add_candidate():
    """
    Add a candidate
    """
    candidate_json_data = frappe.request.get_json()
    candidate_json_data["candidate_name"] = candidate_json_data["name"]
    experiences = []
    try:
        if candidate_json_data.get("experience"):
            if isinstance(candidate_json_data["experience"], str):
                experiences = candidate_json_data["experience"].split(",")
            candidate_json_data.pop("experience")
        candidate = frappe.new_doc("Candidate")
        candidate.update(candidate_json_data)
        for e in experiences:
                candidate.append(
                    "experience_table",
                    {
                        "experience": e,
                    },
                )
        candidate = candidate.save(ignore_permissions=True)
        frappe.response["status"] = "success"
        frappe.response["data"] = candidate.as_dict()
    except Exception as e:
        frappe.response["status"] = "error"
        frappe.response["message"] = str(e)


@frappe.whitelist(allow_guest=True, methods="GET")
def get_candidates():
    """
    Get all the candidates
    """
    candidates = frappe.get_all("Candidate", fields=["name", "email", "status"])
    experiences = frappe.get_all("Experience", fields=["experience", "parent"])
    for candidate in candidates:
        candidate["experience"] = []
        for experience in experiences:
            if candidate["name"] == experience["parent"]:
                candidate["experience"].append(experience["experience"])
    frappe.response["status"] = "success"
    frappe.response["data"] = candidates


@frappe.whitelist(allow_guest=True, methods="PUT")
def edit_candidates():
    """
    Edit a candidate
    """
    candidate_json_data = frappe.request.get_json()
    try:
        candidate = frappe.get_doc("Candidate", candidate_json_data["name"])
        if candidate_json_data.get("experience"):
            if isinstance(candidate_json_data["experience"], str):
                exp = candidate_json_data["experience"].split(",")
            for e in exp:
                candidate.append(
                    "experience_table",
                    {
                        "experience": e,
                    },
                )
            candidate_json_data.pop("experience")
        candidate.update(candidate_json_data)
        candidate = candidate.save(ignore_permissions=True)
        frappe.response["status"] = "success"
        frappe.response["data"] = candidate.as_dict()
    except Exception as e:
        frappe.response["status"] = "error"
        frappe.response["message"] = str(e)
