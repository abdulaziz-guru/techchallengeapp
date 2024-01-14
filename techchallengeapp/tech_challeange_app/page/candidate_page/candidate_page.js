frappe.pages['candidate-page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Candidate',
		single_column: true
	});

	let $btn = page.set_primary_action(__("Add Candidate"), async function () {
		await create_new();
	});

	frappe.breadcrumbs.add("Setup");

	$(frappe.render_template("candidate_page")).appendTo(page.body.addClass("no-border"));

	const editButtons = document.getElementsByTagName("button")
	for (let b of editButtons) {
		if (!b.id) {
			continue;
		}
		b.addEventListener("click", async (e) => {await edit(e.target.id)})
	}
}

async function create_new() {
	// Create the Dialog
	let d = new frappe.ui.Dialog({
		title: "New Candidate",
		fields: await get_fields(),
		size: 'large', // small, large, extra-large 
		primary_action_label: 'Save',
		async primary_action(values) {
			values["doctype"] = "Candidate";
			await frappe.call({
				type: "POST",
				method: "frappe.client.save",
				args: {
					doc: values
				},
				callback: function (r) {
					console.log(r.message);
					//show_alert with indicator for success
					frappe.show_alert({
						message:__('Candidate Saved Successfully'),
						indicator:'green'
					}, 5);
					frappe.confirm("Candidate Saved Successfully. Reload Page?", () => {window.location.reload();})
				},
				error: (r) => {
					console.log(r);
					//show_alert with indicator for failure
					frappe.show_alert({
						message:__('Something went wrong'),
						indicator:'red'
					}, 5);
				}
			});
			d.hide();
		}
	});
	d.show();
}

async function get_fields() {
	var fields = [];
	await frappe.call({
		method: "techchallengeapp.api.get_fields",
		args: {"doctype": "Candidate"},
		callback: (r) => {
			fields = r.message;
		},
		error: (r) => {
			console.log(r);
		}
	});
	return fields;
}


async function get_fields_and_data(id) {
	var fields = await get_fields();
	await frappe.call({
        method: "frappe.client.get",
        type: "GET",
        args: { doctype: "Candidate", filters: {"name": id} },
        callback: (r) => {
			fields = fields.map((f) => {
				if (!in_list(["Section Break", "Column Break", "Tab Break"], f.fieldtype)) {
					// Handle table field
					if (f.fieldtype === "Table") {
						f["data"] = r.message[f.fieldname];
					}
					else {
						f["default"] = r.message[f.fieldname];
					}
				}
				return f;
			});
		}
	});
	return fields;
}


async function edit(id) {
	let d = new frappe.ui.Dialog({
		title: id,
		fields: await get_fields_and_data(id),
		size: 'large', // small, large, extra-large 
		primary_action_label: 'Save',
		async primary_action(values) {
			values["doctype"] = "Candidate";
			await frappe.call({
				type: "PUT",
				method: "frappe.client.set_value",
				args: {
					doctype: "Candidate",
					name: id,
					fieldname: values
				},
				callback: async function (r) {
					console.log(r.message);
					//show_alert with indicator for success
					await frappe.show_alert({
						message:__('Candidate Saved Successfully'),
						indicator:'green'
					}, 5);
					frappe.confirm("Candidate Saved Successfully. Reload Page?", () => {window.location.reload();})
				},
				error: (r) => {
					console.log(r);
					//show_alert with indicator for failure
					frappe.show_alert({
						message:__('Something went wrong'),
						indicator:'red'
					}, 5);
				}
			});
			d.hide();
		}
	});
	d.show();
}
