package com.temenos.ragclient.data

/**
 * Shared Configuration for Temenos RAG Client
 * This file contains shared configurations that should be used by both the Python script and Android app
 * to ensure consistency across platforms.
 */
object SharedConfig {
    
    // Category to Model mapping (shared between Python and Android)
    val CATEGORY_TO_MODEL = mapOf(
        // Generic
        "Temenos Annual Reports" to "InvestorRelations",
        "Policies" to "TemenosPolicies",
        
        // Technology
        "Analytics" to "Analytics",
        "Payments Hub" to "FuncPaymentsHub",
        "Transact" to "TechnologyOverview",
        "TAP" to "TechTAP",
        "Digital" to "digital_model",
        "Modular Banking" to "ModularBanking",
        "Data Hub" to "DataHub",
        "Data Source" to "DataSource",
        "Extensibility Framework" to "ExtensibilityAdvisor",
        "Security" to "SecurityFramework",
        "SaaS" to "SaaSUniformTerms",
        
        // Functionality
        "Transact Wealth" to "FuncTransactWealth",
        "FCM" to "FuncFCM",
        "TAP Wealth" to "funcWealthTAP",
        "Payments" to "Payments",
        "Transact Generic" to "FuncTransactGeneric"
    )
    
    // Categories organized by type (shared structure)
    val CATEGORIES = mapOf(
        "Generic" to listOf("Temenos Annual Reports", "Policies"),
        "Technology" to listOf("Analytics", "Payments Hub", "Transact", "TAP", "Digital", 
                              "Modular Banking", "Data Hub", "Data Source", "Extensibility Framework", 
                              "Security", "SaaS"),
        "Functionality" to listOf("Transact Wealth", "FCM", "TAP Wealth", "Payments", "Transact Generic")
    )
    
    // Available models by region (shared)
    val MODELS_BY_REGION = mapOf(
        "global" to listOf(
            "InvestorRelations", "Analytics", "Payments", "DataHub", "TechnologyOverview",
            "ExtensibilityAdvisor", "SaaSUniformTerms", "SecurityFramework", "ModularBanking",
            "DataSource", "FactSheets", "FuncTransactWealth", "TemenosPolicies",
            "FuncFCM", "digital_model", "funcWealthTAP", "TechTAP", "FuncPaymentsHub",
            "FuncTransactGeneric"
        ),
        "mea" to listOf(
            "PlatformFrameworkMea", "ExtensibilityMea", "DataMea", "SecurityMea",
            "SaaSMea", "TransactMea", "PaymentsMea", "FcmMea", "AnalyticsMea",
            "FinancialInclusionMea", "TacMea", "IslamicMea", "RiskMea", "AIMea",
            "DigitalMea", "PoliciesMea", "ModelBankMea"
        ),
        "us" to listOf(
            "VendorProfileUs", "SupportUs", "TransactUs", "LMSCollectionsUs"
        ),
        "comprehensive" to listOf(
            "AllGlobalModels", "AllMEAModels", "AllUSModels", "AllModels"
        )
    )
    
    // API Configuration (shared)
    val API_CONFIG = mapOf(
        "base_url" to "https://tbsg.temenos.com/api/v1.0",
        "jwt_token" to "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYXBvc3RvbG9zLmdlb3JnYXMiLCJlbWFpbCI6ImFwb3N0b2xvcy5nZW9yZ2FzQHRlbWVub3MuY29tIiwiZXhwIjoxNzU5NDg5MDI5LCJpYXQiOjE3NTY4OTcwMjksImlzcyI6InRic2cudGVtZW5vcy5jb20iLCJhdWQiOiJ0ZW1lbm9zLWFwaSJ9.kaFMG7NQo3hnco_UO3WyjDwGUfrDrgoVFYVJ-vnoQD0",
        "timeout" to 30
    )
    
    // UI Configuration (shared)
    val UI_CONFIG = mapOf(
        "regions" to listOf("Global", "MEA", "Americas"),
        "region_values" to listOf("global", "mea", "us"),
        "context_placeholder" to "Enter additional context for the AI (optional)...",
        "context_instructions" to "Add below any context you wish to send to the Large Language Model. The context could be details about your opportunity, instructions to answer in a specific manner, using specific terminology etc."
    )
    
    /**
     * Get available categories for a specific region
     */
    fun getAvailableCategoriesForRegion(region: String): List<String> {
        val availableModels = MODELS_BY_REGION[region] ?: emptyList()
        val availableCategories = mutableListOf<String>()
        
        for ((_, categories) in CATEGORIES) {
            for (category in categories) {
                val model = CATEGORY_TO_MODEL[category]
                if (model != null && model in availableModels) {
                    availableCategories.add(category)
                }
            }
        }
        
        return availableCategories
    }
    
    /**
     * Get the model ID for a given category
     */
    fun getModelForCategory(category: String): String {
        return CATEGORY_TO_MODEL[category] ?: ""
    }
    
    /**
     * Get the category number mapping for a region (for display purposes)
     */
    fun getCategoryNumberMapping(region: String): Map<Int, String> {
        val availableCategories = getAvailableCategoriesForRegion(region)
        return availableCategories.mapIndexed { index, category -> 
            index + 1 to category 
        }.toMap()
    }
    
    /**
     * Validate category selection and return (isValid, selectedCategory, modelId)
     */
    fun validateCategorySelection(region: String, categoryNumber: Int): Triple<Boolean, String, String> {
        val availableCategories = getAvailableCategoriesForRegion(region)
        
        return if (categoryNumber in 1..availableCategories.size) {
            val selectedCategory = availableCategories[categoryNumber - 1]
            val modelId = getModelForCategory(selectedCategory)
            Triple(true, selectedCategory, modelId)
        } else {
            Triple(false, "", "")
        }
    }
} 