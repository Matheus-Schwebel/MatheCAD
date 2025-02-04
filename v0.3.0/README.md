# Disponibilidade de recursos
> **Versão 0.3.0**
####
<b style="color: red">Em andamento...</b>

| Recurso | Comando | Opções | Obsoleto |
|--------|------|-----|-------|
| ... | ... | ... | ... |

# Exemplos de código
```python
# Criando a primeira quadra com zoneamento residencial
quadra1 = Quadra(100, 100, 400, 200, scene, zone_colors)
quadra1.zone = "residential"  # Zoneamento residencial
quadra1.desenha_quadra()
quadra1.create_terrains()

draw_roundabout(525, 75, 12)
#quadrainter.desenha_quadra()
#quadrainter.create_terrains()


# Criando a segunda quadra com zoneamento comercial
quadra2 = Quadra(550, 100, 400, 200, scene, zone_colors)
quadra2.zone = "commercial"  # Zoneamento comercial
quadra2.desenha_quadra()
quadra2.create_terrains(num_plots=4, margin=10) 
draw_independent_line(550, 186, 400, 30, scene)

# Criando a terceira quadra com zoneamento comercial
quadra3 = Quadra(550, -150, 400, 200, scene, zone_colors)
quadra3.zone = "commercial"  # Zoneamento comercial
quadra3.desenha_quadra()
quadra3.create_terrains(num_plots=4, margin=10) 
draw_independent_line(550, -68, 400, 30, scene)

draw_independent_line(100, -68, 400, 30, scene)


# Criando a quarta quadra com zoneamento residencial
quadra4 = Quadra(100, -150, 400, 200, scene, zone_colors)
quadra4.zone = "residential"  # Zoneamento residencial
quadra4.desenha_quadra()
quadra4.create_terrains()

draw_independent_line(100, 186, 400, 30, scene)
draw_independent_line(100, -68, 400, 30, scene)

```
