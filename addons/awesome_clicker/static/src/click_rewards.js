/** @odoo-module */

export const rewards = [
  {
    description: "Get 1000 click bot",
    apply(clicker) {
      clicker.increment(1000);
    },
    maxLevel: 3,
  },
  {
    description: "Get 10 click bot",
    apply(clicker) {
      clicker.increment(10);
    },
    minLevel: 3,
    maxLevel: 4,
  },
  {
    description: "Increase bot power!",
    apply(clicker) {
      clicker.multipler += 1;
    },
    minLevel: 3,
  },
];
