export interface OrderItem {
  product: String;
  size: String;
  quantity: Number;
}

export interface Order {
  id: String;
  order: OrderItem[];
  created: Date;
  status: String;
}