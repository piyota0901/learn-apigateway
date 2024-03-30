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

export enum Size {
  Small = 'Small',
  Medium = 'Medium',
  Large = 'Large'
}

export interface Product {
  product: String;
  sizes: Size[];
  quantity: Number;
}