variable "subscription_id" {
  type        = string
  description = "ID de l'abonnement Azure for Students (fourni via TF_VAR_subscription_id)"
}

variable "location" {
  type        = string
  default     = "spaincentral"
  description = "Région autorisée pour l'abonnement étudiant (Madrid)"
}

variable "prefix" {
  type        = string
  default     = "devsecops"
  description = "Préfixe des noms de ressources"
}

variable "node_vm_size" {
  type        = string
  default     = "Standard_B2s_v2"
  description = "Taille du nœud : 2 vCPU, 8 Go de RAM"
}
