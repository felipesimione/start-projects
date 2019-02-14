# instalação do pacote arules
install.packages("arules")
install.packages("arulesViz")
library(arules)
library(arulesViz)

# leitura das transacoes com headers "t"(pedido) e "p"(produto)
products = read.transactions("C:/Users/felipe.simione/Desktop/Lambda3/DESAFIO8/online_retail_uk.csv"
                             , format = "single", sep = ";", cols = c("InvoiceNo", "Description"))

# algoritmo apriori com confiança mínima=0.1 e suporte mínimo=0.0001
products.apriori <- apriori(products, parameter=list(support=0.01, confidence = 0.1))
# inspect(sort(products.apriori, by=c("support","confidence"))[1:20])
inspect(sort(products.apriori, by="lift")[1:10])

# plot do gráfico
products_graph.apriori <- apriori(products, parameter=list(support=0.01, confidence = 0.1,  minlen=2, maxlen =4),appearance = list(lhs=c("REGENCY TEA PLATE GREEN"), default = "rhs"))
inspect(sort(products_graph.apriori, by="lift")[1:4])
plot(products_graph.apriori,method="graph")
