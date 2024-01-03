/** @odoo-module **/

import { useState, Component, markup } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.Card";
  static props = {
    title: String,
    slots: {
      type: Object,
      shape: {
        default: true,
        title: true,
      },
    },
  };
  setup() {
    this.isOpen = useState({ value: true });
  }
  onToggle() {
    this.isOpen.value = !this.isOpen.value;
  }
}
