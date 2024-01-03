/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todoitem/todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };
  setup() {
    this.todos = useState([]);
    useAutofocus("input");
  }

  addTodo(ev) {
    if (ev.keyCode === 13) {
      if (ev.target.value != "") {
        this.todos.push({
          id: this.todos.length + 1,
          description: ev.target.value,
          isCompleted: false,
        });
        ev.target.value = "";
      }
    }
  }
  toggleState(id) {
    this.todos.forEach((el) => {
      if (el.id == id) {
        el.isCompleted = !el.isCompleted;
      }
    });
  }
  removeTodo(id) {
    const index = this.todos.findIndex((elem) => elem.id === id);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  }
}
