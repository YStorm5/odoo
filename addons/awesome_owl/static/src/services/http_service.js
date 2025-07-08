/** @odoo-module **/

import { registry } from "@web/core/registry";

async function get(route) {
    const res = await fetch(route, {
        method: "GET",
    });
    const data = await res.json();
    return data;
}

async function post(route, token, body) {
    const res = await fetch(route, {
        method: "POST",
        body: body,
        headers: {
            "Content-type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });
    const data = await res.json();
    return data;
}

const httpService = {
    start(_env) {
        return { get, post };
    },
};

registry.category("services").add("fetch", httpService);
