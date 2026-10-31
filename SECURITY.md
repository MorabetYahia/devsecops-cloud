# Politique de sécurité

## Signaler une vulnérabilité

Merci de **ne pas ouvrir d'issue publique**. Utilisez l'onglet **Security → Report a vulnerability** de ce dépôt (signalement privé GitHub). Une réponse est apportée sous 7 jours.

## Contrôles automatiques

Chaque push et chaque Pull Request passent par le pipeline [`deploy.yml`](.github/workflows/deploy.yml) :

| Contrôle | Outil | Bloquant |
|---|---|---|
| Tests applicatifs | pytest | Oui |
| Secrets dans l'historique Git | Gitleaks | Oui |
| Analyse statique du code (SAST) | Semgrep | Oui |
| Configuration Terraform / Kubernetes / Dockerfile | Checkov | Non (résultats dans l'onglet Security) |
| Vulnérabilités de l'image (CVE CRITICAL/HIGH corrigeables) | Trivy | Oui |

Les dépendances, les actions GitHub et l'image de base sont surveillées par **Dependabot**. Les actions tierces sont épinglées par SHA de commit.

## Périmètre

Projet de démonstration déployé sur une infrastructure éphémère : l'environnement n'existe que pendant les sessions de travail.
