# Accessibilité

## Guides de développement

Des guides permettent la prise en compte de l'accessibilité numérique dans les développements :

* [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/fr)
* [RGAA](https://accessibilite.numerique.gouv.fr/)
* Notices d'intégration de [AcceDe Web](https://www.accede-web.com/notices/html-et-css/)

## Recommandations

* Ecrire un test spécifique pour **chaque composant**, **chaque parent** et au niveau de **la page** et/ou de **l'onglet**.
* Inclure les tests automatique d'accessibilité comme étape de l'intégration continue (CI)

## Outils et pratiques

* [Lighthouse](https://github.com/GoogleChrome/lighthouse) permet de vérifier le niveau d'accessibilité.
* Pour les projets en TS, certains plugins [Eslint](https://eslint.org/) permettent de s'assurer automatiquement que les régles d'accessibilité sont respectées (ex : [react-a11y](https://github.com/reactjs/react-a11y)).
  * Compléter les tests unitaires et d'intégration avec l'utilisation de [jest-axe](https://www.npmjs.com/package/jest-axe) dans le cas où [Jest](https://jestjs.io/) est utilisé.

---
