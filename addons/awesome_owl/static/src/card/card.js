/** @odoo-module **/

import { useState, Component, markup } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        estate: Object,
    };
    setup() {
        this.isOpen = useState({ value: false });
        this.estate = this.props.estate;
    }
    onToggle() {
        this.isOpen.value = !this.isOpen.value;
    }
}
