# Disponibilidade de recursos
> **Versão 0.1**

[Download](https://github.com/Matheus-Schwebel/MatheCAD/blob/main/v0.2.0.git)

####
A disponibilidade nesta versão é mais limitada. Confira:

| Recurso | Comando | Opções | Obsoleto
|--------|------|-----|-------|
| Zoneamento | Quadra().zone() | Residential (padrão), commercial, park, industrial | Não |
| Rotatórias | Quadra().create_roundabout() | x, y, radius | Sim |
| Rotatórias | draw_roundabout() | x, y, radius | Não |

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
