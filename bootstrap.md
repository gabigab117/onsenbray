/Users/gabrieltrouve/Pro/onsenbray/project/static/scss/custom-bootstrap.scss
/Users/gabrieltrouve/Pro/onsenbray/project/static/css/bootstrap-custom.css

## 🎨 Utilisation des couleurs

Vous avez maintenant accès à **toutes les variantes** :

### Couleurs de fond (background)

```html
<div class="bg-blue-100">Bleu très clair</div>
<div class="bg-blue-500">Bleu standard</div>
<div class="bg-blue-900">Bleu très foncé</div>

<div class="bg-purple-300">Violet clair</div>
<div class="bg-indigo-600">Indigo</div>
<div class="bg-cyan-200">Cyan clair</div>
```

### Couleurs de texte

```html
<p class="text-blue-900">Texte bleu foncé</p>
<p class="text-purple-500">Texte violet</p>
<p class="text-green-700">Texte vert</p>
```

### Couleurs de bordure

```html
<div class="border border-3 border-red-400">Bordure rouge claire</div>
<div class="border border-purple-600">Bordure violette</div>
```

### Mix de couleurs

```html
<div class="bg-cyan-100 text-cyan-900 border border-cyan-600 p-4">
    Fond cyan clair, texte foncé, bordure moyenne
</div>
```

### Boutons personnalisés

```html
<button class="btn bg-indigo-600 text-white">Mon bouton</button>
<button class="btn bg-pink-500 text-white">Bouton rose</button>
```

## 📚 Couleurs disponibles

Chaque couleur a 9 nuances (100 à 900) :

- **Bleus** : `blue-100` à `blue-900`
- **Indigo** : `indigo-100` à `indigo-900`
- **Violet** : `purple-100` à `purple-900`
- **Rose** : `pink-100` à `pink-900`
- **Rouge** : `red-100` à `red-900`
- **Orange** : `orange-100` à `orange-900`
- **Jaune** : `yellow-100` à `yellow-900`
- **Vert** : `green-100` à `green-900`
- **Teal** : `teal-100` à `teal-900`
- **Cyan** : `cyan-100` à `cyan-900`
- **Gris** : `gray-100` à `gray-900`

Plus les **8 couleurs thématiques** par défaut :
- `primary`, `secondary`, `success`, `danger`, `warning`, `info`, `light`, `dark`

## 🚢 Déploiement sur VPS

**Aucune installation npm nécessaire sur le VPS !**

1. Le CSS compilé (`bootstrap-custom.css`) est committé dans Git
2. Sur le VPS : `git pull`
3. Django sert le fichier CSS statique normalement
4. C'est tout ! ✅