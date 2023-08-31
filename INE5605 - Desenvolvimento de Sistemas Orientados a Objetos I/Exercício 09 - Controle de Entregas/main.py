from pedido import Pedido
from cliente import Cliente
from item_pedido import ItemPedido
from tipo_pedido import TipoPedido
from cliente_fidelidade import ClienteFidelidade
from controlador_pedidos import ControladorPedidos



cliente1 = Cliente("123", "Lucas", "Rua", "321")
cliente2 = ClienteFidelidade(123, 0.3, "sad", "ddd", "asd", "sad")
tipo = TipoPedido("Paster", 5)
p1 = Pedido(123, cliente2, tipo)
p2 = Pedido(123, cliente1, tipo)
p1.inclui_item_pedido(123, "abc", 10)
#print(p1.exclui_item_pedido(123))
#print(p1.exclui_item_pedido(333))
print(p2.calcula_valor_pedido(10))
print(p1.calcula_valor_pedido(10))


