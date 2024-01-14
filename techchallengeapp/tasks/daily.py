"""This module contains daily tasks"""

import frappe


def remove_candidate():
    # DELETE candidate with "Rejected" status
    frappe.db.delete("Candidate", {"status": "Rejected"})
