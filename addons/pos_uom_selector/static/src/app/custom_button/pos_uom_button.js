/**@odoo-module **/
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component, markup, xml } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Dialog } from "@web/core/dialog/dialog";

class UOMSelectorDialogBody extends Component {
  static components = { Dialog };
  static props = ["uomMap"];

  setup() {
    this.pos = usePos();
    this.uomMap = this.props.uomMap;
  }
  static template = xml`
  <Dialog size="'md'" title="'Select Unit of Measure'">
    <div class="d-flex justify-content-evenly">
      <t t-foreach="uomMap" t-as="uom" t-key="uom.id">
        <button class="btn btn-primary" t-on-click="() => this.select(uom)">
          <div class="d-flex">
            <span>$</span>
            <span> </span>
            <span><t t-esc="uom.price.toFixed(2)"/>/<t t-esc="uom.name"/></span>
          </div>
        </button>
      </t>
    </div>
  </Dialog>
`;

  select(uom) {
    const order = this.pos.get_order();
    const line = order.get_selected_orderline();

    if (line) {
      line.product_uom2_id = uom["id"][0];
      line.price_type = "manual";
      line.set_unit_price(uom["price"]);
    }
  }
}

export class CreateButton extends Component {
  static template = "point_of_sale.CreateButton";
  setup() {
    this.pos = usePos();
    this.dialog = useService("dialog");
    this.uomMap = this.loadAllMultiUOM();
  }

  async onClick() {
    if (this.loadUnitSelect().length !== 0) {
      this.dialog.add(UOMSelectorDialogBody, {
        uomMap: this.loadUnitSelect(),
      });
    }
  }

  loadAllMultiUOM() {
    const uomPrices = this.pos.uom_prices || [];
    return uomPrices;
  }

  loadUnitSelect() {
    const order = this.pos.get_order();
    const line = order.get_selected_orderline();
    const product = line.product;
    const currentUOM = this.pos.units_by_id;
    return this.uomMap
      .filter((prod) => prod.product_tmpl_id[0] == product.product_tmpl_id)
      .map((v) => {
        return {
          id: v.uom_id,
          name: currentUOM[v.uom_id[0]].name,
          price: v.price,
        };
      });
  }
}

ProductScreen.addControlButton({
  component: CreateButton,
});
