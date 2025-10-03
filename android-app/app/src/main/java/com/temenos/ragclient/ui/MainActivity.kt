package com.temenos.ragclient.ui

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.ArrayAdapter
import android.widget.AutoCompleteTextView
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.google.android.material.button.MaterialButton
import com.google.android.material.card.MaterialCardView
import com.google.android.material.chip.Chip
import com.google.android.material.chip.ChipGroup
import com.google.android.material.progressindicator.CircularProgressIndicator
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.google.android.material.textview.MaterialTextView
import com.temenos.ragclient.R
import com.temenos.ragclient.data.QueryRequest
import com.temenos.ragclient.data.Repository
import com.temenos.ragclient.data.SharedConfig
import com.temenos.ragclient.data.Conversation
import com.temenos.ragclient.data.ConversationDatabase
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.*

class MainActivity : AppCompatActivity() {
    
    private lateinit var repository: Repository
    
    // UI Components
    private lateinit var connectionStatus: android.widget.TextView
    private lateinit var testConnectionBtn: MaterialButton
    private lateinit var questionInput: TextInputEditText
    private lateinit var regionRadioGroup: RadioGroup
    private lateinit var globalRadio: RadioButton
    private lateinit var meaRadio: RadioButton
    private lateinit var americasRadio: RadioButton
    private lateinit var contextInput: TextInputEditText
    private lateinit var contextInputLayout: TextInputLayout
    private lateinit var toggleContextButton: MaterialButton
    private lateinit var sendButton: MaterialButton
    private lateinit var responseCard: MaterialCardView
    private lateinit var responseText: android.widget.TextView
    private lateinit var metadataText: android.widget.TextView
    private lateinit var copyButton: MaterialButton
    private lateinit var clearButton: MaterialButton
    private lateinit var progressIndicator: CircularProgressIndicator
    
    // Chip Groups
    private lateinit var genericChipGroup: ChipGroup
    private lateinit var technologyChipGroup: ChipGroup
    private lateinit var functionalityChipGroup: ChipGroup
    
    // Data
    private var selectedRegion = "global"
    private var selectedModel = ""
    private var isContextVisible = true
    private var isConnectionVisible = false  // Hide connection test by default
    private var database: ConversationDatabase? = null
    
    // Use shared configuration
    private val categoryToModel = SharedConfig.CATEGORY_TO_MODEL
    private val modelsByRegion = SharedConfig.MODELS_BY_REGION
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Add crash handler
        Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
            android.util.Log.e("MainActivity", "Uncaught exception in thread ${thread.name}: ${throwable.message}", throwable)
        }
        
        try {
            setContentView(R.layout.activity_main)
            
            // Set up toolbar safely
            val toolbar = findViewById<com.google.android.material.appbar.MaterialToolbar>(R.id.toolbar)
            if (toolbar != null) {
                setSupportActionBar(toolbar)
                supportActionBar?.setDisplayHomeAsUpEnabled(false)
            } else {
                android.util.Log.w("MainActivity", "Toolbar not found")
            }
            
            repository = Repository(this)
            initializeViews()
            setupListeners()
            android.util.Log.d("MainActivity", "About to update connection visibility, isConnectionVisible = $isConnectionVisible")
            updateConnectionVisibility()
            android.util.Log.d("MainActivity", "Connection visibility update completed")
            
            // Ensure connection card is hidden after layout is rendered
            findViewById<View>(R.id.connectionCard)?.post {
                if (!isConnectionVisible) {
                    updateConnectionVisibility()
                    android.util.Log.d("MainActivity", "Post-delayed connection visibility update completed")
                }
            }
        } catch (e: Exception) {
            // Log the error and show a user-friendly message
            android.util.Log.e("MainActivity", "Error during initialization: ${e.message}", e)
            Toast.makeText(this, "Error initializing app: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }
    
    private fun initializeViews() {
        try {
            // Initialize all views with null checks
            connectionStatus = findViewById(R.id.connectionStatus) ?: throw Exception("connectionStatus not found")
            testConnectionBtn = findViewById(R.id.testConnectionBtn) ?: throw Exception("testConnectionBtn not found")
            questionInput = findViewById(R.id.questionInput) ?: throw Exception("questionInput not found")
            regionRadioGroup = findViewById(R.id.regionRadioGroup) ?: throw Exception("regionRadioGroup not found")
            globalRadio = findViewById(R.id.globalRadio) ?: throw Exception("globalRadio not found")
            meaRadio = findViewById(R.id.meaRadio) ?: throw Exception("meaRadio not found")
            americasRadio = findViewById(R.id.americasRadio) ?: throw Exception("americasRadio not found")
            contextInput = findViewById(R.id.contextInput) ?: throw Exception("contextInput not found")
            contextInputLayout = findViewById(R.id.contextInputLayout) ?: throw Exception("contextInputLayout not found")
            toggleContextButton = findViewById(R.id.toggleContextButton) ?: throw Exception("toggleContextButton not found")
            sendButton = findViewById(R.id.sendButton) ?: throw Exception("sendButton not found")
            responseCard = findViewById(R.id.responseCard) ?: throw Exception("responseCard not found")
            responseText = findViewById(R.id.responseText) ?: throw Exception("responseText not found")
            metadataText = findViewById(R.id.metadataText) ?: throw Exception("metadataText not found")
            copyButton = findViewById(R.id.copyButton) ?: throw Exception("copyButton not found")
            clearButton = findViewById(R.id.clearButton) ?: throw Exception("clearButton not found")
            progressIndicator = findViewById(R.id.progressIndicator) ?: throw Exception("progressIndicator not found")
            
            // Chip Groups
            genericChipGroup = findViewById(R.id.genericChipGroup) ?: throw Exception("genericChipGroup not found")
            technologyChipGroup = findViewById(R.id.technologyChipGroup) ?: throw Exception("technologyChipGroup not found")
            functionalityChipGroup = findViewById(R.id.functionalityChipGroup) ?: throw Exception("functionalityChipGroup not found")
            
            android.util.Log.d("MainActivity", "All views initialized successfully")
            
            // Initialize database (optional for now)
            try {
                database = ConversationDatabase.getDatabase(this)
                android.util.Log.d("MainActivity", "Database initialized successfully")
            } catch (e: Exception) {
                android.util.Log.w("MainActivity", "Database initialization failed: ${e.message}")
                // Continue without database for now
            }
        } catch (e: Exception) {
            android.util.Log.e("MainActivity", "Error initializing views: ${e.message}", e)
            throw e
        }
    }
    
    private fun setupListeners() {
        testConnectionBtn.setOnClickListener {
            testConnection()
        }
        
        // Region selection
        regionRadioGroup.setOnCheckedChangeListener { _, checkedId ->
            selectedRegion = when (checkedId) {
                R.id.globalRadio -> "global"
                R.id.meaRadio -> "mea"
                R.id.americasRadio -> "us"
                else -> "global"
            }
            updateAvailableCategories()
        }
        
        // Generic chips
        genericChipGroup.setOnCheckedStateChangeListener { group, checkedIds ->
            if (checkedIds.isNotEmpty()) {
                handleChipSelection(group, checkedIds[0])
            }
        }
        
        // Technology chips
        technologyChipGroup.setOnCheckedStateChangeListener { group, checkedIds ->
            if (checkedIds.isNotEmpty()) {
                handleChipSelection(group, checkedIds[0])
            }
        }
        
        // Functionality chips
        functionalityChipGroup.setOnCheckedStateChangeListener { group, checkedIds ->
            if (checkedIds.isNotEmpty()) {
                handleChipSelection(group, checkedIds[0])
            }
        }
        
        // Context toggle
        toggleContextButton.setOnClickListener {
            toggleContext()
        }
        
        sendButton.setOnClickListener {
            sendQuery()
        }
        
        copyButton.setOnClickListener {
            copyResponse()
        }
        
        clearButton.setOnClickListener {
            clearResponse()
        }
    }
    
    private fun handleChipSelection(group: ChipGroup, checkedId: Int) {
        // Clear other chip groups
        if (group.id != R.id.genericChipGroup) {
            genericChipGroup.clearCheck()
        }
        if (group.id != R.id.technologyChipGroup) {
            technologyChipGroup.clearCheck()
        }
        if (group.id != R.id.functionalityChipGroup) {
            functionalityChipGroup.clearCheck()
        }
        
        // Get selected chip text and map to model
        val selectedChip = findViewById<Chip>(checkedId)
        selectedChip?.let { chip ->
            val categoryName = chip.text.toString()
            selectedModel = SharedConfig.getModelForCategory(categoryName)
        }
    }
    
    private fun updateAvailableCategories() {
        val availableModels = modelsByRegion[selectedRegion] ?: emptyList()
        
        // Enable/disable chips based on available models for the selected region
        for (i in 0 until genericChipGroup.childCount) {
            val view = genericChipGroup.getChildAt(i)
            if (view is Chip) {
                val model = SharedConfig.getModelForCategory(view.text.toString())
                view.isEnabled = model.isNotEmpty() && availableModels.contains(model)
            }
        }
        
        for (i in 0 until technologyChipGroup.childCount) {
            val view = technologyChipGroup.getChildAt(i)
            if (view is Chip) {
                val model = SharedConfig.getModelForCategory(view.text.toString())
                view.isEnabled = model.isNotEmpty() && availableModels.contains(model)
            }
        }
        
        for (i in 0 until functionalityChipGroup.childCount) {
            val view = functionalityChipGroup.getChildAt(i)
            if (view is Chip) {
                val model = SharedConfig.getModelForCategory(view.text.toString())
                view.isEnabled = model.isNotEmpty() && availableModels.contains(model)
            }
        }
        
        // Clear selections when region changes
        genericChipGroup.clearCheck()
        technologyChipGroup.clearCheck()
        functionalityChipGroup.clearCheck()
        selectedModel = ""
    }
    
    private fun toggleContext() {
        isContextVisible = !isContextVisible
        
        if (isContextVisible) {
            contextInputLayout.visibility = View.VISIBLE
            toggleContextButton.text = "▼ Hide Context"
        } else {
            contextInputLayout.visibility = View.GONE
            toggleContextButton.text = "▶ Show Context"
        }
    }
    
    private fun testConnection() {
        // Only test connection if the card is visible
        if (!isConnectionVisible) {
            return
        }
        
        lifecycleScope.launch {
            try {
                connectionStatus.text = "Testing connection..."
                val result = repository.testConnection()
                result.fold(
                    onSuccess = {
                        connectionStatus.text = "✅ Connected successfully"
                        connectionStatus.setTextColor(resources.getColor(R.color.success, null))
                    },
                    onFailure = { exception ->
                        connectionStatus.text = "❌ Connection failed: ${exception.message}"
                        connectionStatus.setTextColor(resources.getColor(R.color.error, null))
                    }
                )
            } catch (e: Exception) {
                connectionStatus.text = "❌ Connection error: ${e.message}"
                connectionStatus.setTextColor(resources.getColor(R.color.error, null))
            }
        }
    }
    
    private fun sendQuery() {
        val question = questionInput.text.toString().trim()
        val context = contextInput.text.toString().trim()
        
        if (question.isEmpty()) {
            Toast.makeText(this, "Please enter a question", Toast.LENGTH_SHORT).show()
            return
        }
        
        if (selectedModel.isEmpty()) {
            Toast.makeText(this, "Please select a category", Toast.LENGTH_SHORT).show()
            return
        }
        
        lifecycleScope.launch {
            try {
                showLoading(true)
                
                val request = QueryRequest(
                    question = question,
                    region = selectedRegion,
                    RAGmodelId = selectedModel,
                    context = context
                )
                
                val result = repository.queryRAG(request)
                result.fold(
                    onSuccess = { response ->
                        if (response.status == "success" && response.data != null) {
                            showResponse(response.data.answer, response.data, response.metadata)
                        } else {
                            showError("Query failed: ${response.error ?: "Unknown error"}")
                        }
                    },
                    onFailure = { exception ->
                        showError("Query failed: ${exception.message}")
                    }
                )
            } catch (e: Exception) {
                showError("Query error: ${e.message}")
            } finally {
                showLoading(false)
            }
        }
    }
    
    private fun showLoading(show: Boolean) {
        progressIndicator.visibility = if (show) View.VISIBLE else View.GONE
        sendButton.isEnabled = !show
    }
    
    private fun showResponse(answer: String, data: com.temenos.ragclient.data.QueryData, metadata: com.temenos.ragclient.data.Metadata?) {
        responseText.text = answer
        responseCard.visibility = View.VISIBLE
        
        val metadataString = buildString {
            appendLine("Model: ${data.model_id}")
            appendLine("Region: ${data.region}")
            appendLine("Context used: ${data.context_used}")
            metadata?.let {
                appendLine("API Version: ${it.api_version ?: "N/A"}")
                appendLine("Timestamp: ${it.timestamp ?: "N/A"}")
                appendLine("Response length: ${it.response_length ?: "N/A"}")
            }
        }
        metadataText.text = metadataString
    }
    
    private fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show()
    }
    
    private fun copyResponse() {
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        val clip = ClipData.newPlainText("Temenos RAG Response", responseText.text)
        clipboard.setPrimaryClip(clip)
        Toast.makeText(this, "Response copied to clipboard", Toast.LENGTH_SHORT).show()
    }
    
    private fun clearResponse() {
        responseCard.visibility = View.GONE
        questionInput.text?.clear()
        contextInput.text?.clear()
        genericChipGroup.clearCheck()
        technologyChipGroup.clearCheck()
        functionalityChipGroup.clearCheck()
        selectedModel = ""
    }
    
    // Menu handling
    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        try {
            menuInflater.inflate(R.menu.menu_main, menu)
            
            // Update menu item titles
            val toggleConnectionItem = menu.findItem(R.id.action_toggle_connection)
            toggleConnectionItem?.title = if (isConnectionVisible) getString(R.string.hide_connection) else getString(R.string.show_connection)
            
            val darkModeItem = menu.findItem(R.id.action_dark_mode)
            val isDarkMode = resources.configuration.uiMode and 
                android.content.res.Configuration.UI_MODE_NIGHT_MASK == 
                android.content.res.Configuration.UI_MODE_NIGHT_YES
            darkModeItem?.title = if (isDarkMode) getString(R.string.light_mode) else getString(R.string.dark_mode)
            
            return true
        } catch (e: Exception) {
            android.util.Log.e("MainActivity", "Error creating options menu: ${e.message}", e)
            return false
        }
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_toggle_connection -> {
                toggleConnectionVisibility()
                true
            }
            R.id.action_dark_mode -> {
                toggleDarkMode()
                true
            }
            R.id.action_history -> {
                startHistoryActivity()
                true
            }
            R.id.action_settings -> {
                startSettingsActivity()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
    
    private fun updateMenuItems() {
        // Menu items will be updated when the menu is created
    }
    
    private fun toggleConnectionVisibility() {
        isConnectionVisible = !isConnectionVisible
        updateConnectionVisibility()
        invalidateOptionsMenu()
        
        // If we just made the connection card visible, reset status and test the connection
        if (isConnectionVisible) {
            connectionStatus.text = "Ready to test"
            connectionStatus.setTextColor(resources.getColor(R.color.text_secondary, null))
            testConnection()
        }
    }
    
    private fun updateConnectionVisibility() {
        try {
            val connectionCard = findViewById<View>(R.id.connectionCard)
            if (connectionCard != null) {
                val newVisibility = if (isConnectionVisible) View.VISIBLE else View.GONE
                connectionCard.visibility = newVisibility
                android.util.Log.d("MainActivity", "Connection card visibility set to: ${if (isConnectionVisible) "VISIBLE" else "GONE"}")
            } else {
                android.util.Log.e("MainActivity", "Connection card not found")
            }
        } catch (e: Exception) {
            android.util.Log.e("MainActivity", "Error updating connection visibility: ${e.message}", e)
        }
    }
    
    private fun toggleDarkMode() {
        try {
            val currentMode = resources.configuration.uiMode and 
                android.content.res.Configuration.UI_MODE_NIGHT_MASK
            val newMode = if (currentMode == android.content.res.Configuration.UI_MODE_NIGHT_YES) {
                androidx.appcompat.app.AppCompatDelegate.MODE_NIGHT_NO
            } else {
                androidx.appcompat.app.AppCompatDelegate.MODE_NIGHT_YES
            }
            androidx.appcompat.app.AppCompatDelegate.setDefaultNightMode(newMode)
            invalidateOptionsMenu()
        } catch (e: Exception) {
            android.util.Log.e("MainActivity", "Error toggling dark mode: ${e.message}", e)
            Toast.makeText(this, "Error changing theme", Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun startHistoryActivity() {
        val intent = android.content.Intent(this, HistoryActivity::class.java)
        startActivity(intent)
    }
    
    private fun startSettingsActivity() {
        val intent = android.content.Intent(this, SettingsActivity::class.java)
        startActivity(intent)
    }
} 