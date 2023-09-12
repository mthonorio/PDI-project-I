# Filtros e Correlação de Processamento e Digitalização de Imagem

Este projeto foi desenvolvido com técnicas de filtros e correlação de imagens para a disciplina de Processamento e Digitalização de Imagem do semestre 2022.2 ministrada pelo professor Leonardo Vidal Batista.

## Especificação do projeto

Desenvolva, em uma linguagem de programação de sua escolha, um sistema para abrir,
exibir, manipular e salvar imagens RGB com 24 bits/pixel (8 bits/componente/pixel). Não
use bibliotecas ou funções especiais de processamento de imagens. O sistema deve ter a
seguinte funcionalidade:

1. Conversão RGB-YIQ-RGB (cuidado com os limites de R, G e B na volta!).
2. Negativo. Duas formas de aplicação devem ser testadas: em RGB (banda a banda) e
   na banda Y, com posterior conversão para RGB.
3. Correlação m x n (inteiros não negativos), com extensão por zeros, sobre R, G e B,
   com offset (inteiro) e filtro definidos em um arquivo (txt) à parte. Testar com filtros
   Soma, Box, ||Sobel|| e Emboss, e explicar os resultados. Compare
   Box11x1(Box1x11(Image)) com Box(11x11), em termos de resultado e tempo de
   processamento. Para o Sobel, aplique expansão de histograma para [0, 255]. Para o
   filtro de Emboss, aplique valor absoluto ao resultado da correlação, e então some o
   offset.
4. Filtro mediana m x n, com m e n ímpares, sobre R, G e B.

## Módulos

- **get_negative_pixels**: Captura todos os pixels da imagem, separa suas cores em listas e converte subtraindo o valor 255 do valor de cada cor, ou seja, faz a subtração para o (Red, Green and Blue) da imagem e retorna o resultado em uma lista de listas.
- **turn_negative**: Chama a função (get_negative_pixels), itera transformando os pixels retornados em imagem e retorna a imagem.
- **rgb_to_yiq**: Recebe uma imagem RGB e cria os ajustes necessários para converter os pixels para YIQ utilizando uma fórmula correta para isso. O retorno da função é uma lista de listas, sendo uma lista para Y, uma para I e outra para Q. 
- **get_rpg_pixels_from_yiq**: Recebe a lista de listas da função rgb_to_yiq no formato de YIQ, converte e retorna em formato RGB.
- **yiq_to_rgb**: Recebe uma lista de listas de uma lista do tipo float como parâmetro e retorna um objeto do tipo Image. Por fim, também é o responsável por rotacionar a imagem à sua posição original. 
- **negative_on_y**: Chama a função de RGB to YIQ para a imagem e aplica o negativo no Y e retorna a imagem em RGB novamente.
- **median_ixj**: Função de tratamento que chama a função principal da mediana. ```median ixj``` e verificar se os
valores de i e de j são ímpares.
- **median_filter**: O filtro mediana vai fazer com que os valores de RGB da imagem sejam atualizados com a mediana calculada pela função np.median().
- **call_correlation_mxn**: Valida se os valores passados de m x n são validos, caso sejam, passa os parâmetros e retorna a função de correlational.
- **correlational**: Aplica o filtro de correlação na imagem através da manipulação de pixels utilizando a numpy e retorna uma imagem.
- **histogram_expansion**: Aumenta o contraste da imagem somente após a mesma utilizar o filtro de Sobel.  
- **read_correlational_filters**: Função que ler todos os arquivos TXT da pasta de testes com os parâmetros de filtros escritos e seus devidos offsets, trata os dados dos filtros, aplica na imagem cada filtro pixel a pixel e retorna uma imagem.

## Execução

Para a execução do projeto basta executar no terminal:

```
python main.py
```

## Colaboradores

| <a href="https://www.linkedin.com/in/jhonata-ezequiel-alves-de-miranda/" target="_blank">**Jhonata Ezequiel**</a> | <a href="https://www.linkedin.com/in/matheushonorio" target="_blank">**Matheus Honório**</a> |                                                  <a href="https://www.linkedin.com/in/victoria-monteiro-pontes/" target="_blank">**Victoria Monteiro**</a>                                                   |
| :---------------------------------------------------------------------------------------------------------------: |  :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-:
|               <img src="https://avatars.githubusercontent.com/u/57595331?v=4" width="200px"> </img>               |    <img src="https://avatars.githubusercontent.com/u/52137826?v=4" width="200px"> </img>     | <img src="https://media.licdn.com/dms/image/C4D03AQGa5dfKibulxw/profile-displayphoto-shrink_200_200/0/1636472208301?e=1687392000&v=beta&t=-U1gGR5AMnO7caqwe-kugqTJQwXH7dynzES7tdJ9rfE" width="200px"> </img> | 
|           <a href="https://github.com/JhonataEzequiel" target="_blank">`github.com/JhonataEzequiel`</a>           |    <a href="https://github.com/mthonorio" target="_blank">`github.com/MatheusHonorio`</a>    |                                                            <a href="https://github.com/vmp309" target="_blank">`github.com/VictoriaMonteiro`</a>                                                             |     |
