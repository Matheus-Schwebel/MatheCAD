# MatheCAD
> **Versão 0.1**<br>
####
O MatheCAD é projetado para você fazer projetos de cidades gratuitamente e em um App leve.
# Como Executar?
Execute em seu terminal:
```shell
pip install pyqt5
```

E, em seguida:
```shell
py mathecad.py
```
# Disponibilidade de recursos
> **Versão 0.1**
####
A disponibilidade nesta versão é mais limitada. Confira:

| Recurso | Comando | Opções |
|--------|------|-----|
| Zoneamento | Quadra().zone() | Residential (padrão), commercial, park, industrial|

# Exemplos de código
```python
# Criando a primeira quadra com zoneamento residencial
quadra1 = Quadra(100, 100, 400, 200, scene, zone_colors)
quadra1.zone = "residential"  # Zoneamento residencial
quadra1.desenha_quadra()
quadra1.create_terrains()

# Criando a segunda quadra com zoneamento comercial
quadrainter = Quadra(500, 100, 400, 200, scene, zone_colors)
quadrainter.zone = "park"  # Zoneamento park
quadrainter.create_roundabout(525, 100, 12)
#quadrainter.desenha_quadra()
#quadrainter.create_terrains()


# Criando a segunda quadra com zoneamento comercial
quadra2 = Quadra(550, 100, 400, 200, scene, zone_colors)
quadra2.zone = "commercial"  # Zoneamento comercial
quadra2.desenha_quadra()
quadra2.create_terrains()
```
