-- Create a trigger to update table items when an order is placed
DELIMITER //
CREATE TRIGGER update_items
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
END;//
DELIMITER ;
