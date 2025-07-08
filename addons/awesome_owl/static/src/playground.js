/** @odoo-module **/

import { Component, useState, markup, onMounted, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  static components = { Counter, Card, TodoList };
  setup() {
    this.http = useService("fetch");
    this.str1 = "<div class='text-primary'>some content</div>";
    this.str2 = markup("<div class='text-primary'>some content</div>");
    this.state = useState({
      value: 2,
      name: "",
      estates: [],
    });
    onWillStart(async () => {
      this.state.estates = await this.http.get("http://localhost:8069/estate");
    });
  }
  incrementSum() {
    this.state.value += 1;
  }
}
