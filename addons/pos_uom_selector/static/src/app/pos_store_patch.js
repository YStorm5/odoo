/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline, Product } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
  async _processData(loadedData) {
    await super._processData(loadedData);
    this.uom_prices = loadedData["product.uom.price"] || [];
  },
});

patch(Orderline.prototype, {
  export_as_JSON() {
    const json = super.export_as_JSON();
    json.product_uom2_id = this.product_uom2_id;
    return json;
  },

  init_from_JSON(json) {
    super.init_from_JSON(json);
    this.product_uom2_id = json.product_uom2_id;
  },

  get_unit() {
    const unit = this.pos.units_by_id?.[this.product_uom2_id];
    return unit || super.get_unit();
  },
});
