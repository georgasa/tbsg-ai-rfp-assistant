package com.temenos.ragclient.ui

import android.content.SharedPreferences
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.preference.PreferenceFragmentCompat
import androidx.preference.PreferenceManager
import androidx.preference.SwitchPreferenceCompat
import com.temenos.ragclient.R
import com.temenos.ragclient.data.ConversationDatabase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class SettingsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        try {
            setContentView(R.layout.activity_settings)
            supportFragmentManager
                .beginTransaction()
                .replace(R.id.settings_container, SettingsFragment())
                .commit()
            
            supportActionBar?.setDisplayHomeAsUpEnabled(true)
            title = "Settings"
        } catch (e: Exception) {
            android.util.Log.e("SettingsActivity", "Error during initialization: ${e.message}", e)
            android.widget.Toast.makeText(this, "Error loading settings: ${e.message}", android.widget.Toast.LENGTH_LONG).show()
            finish()
        }
    }
    
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}

class SettingsFragment : PreferenceFragmentCompat(), SharedPreferences.OnSharedPreferenceChangeListener {
    
    override fun onCreatePreferences(savedInstanceState: Bundle?, rootKey: String?) {
        try {
            setPreferencesFromResource(R.xml.preferences, rootKey)
            
            // Set up preference change listener
            preferenceManager.sharedPreferences?.registerOnSharedPreferenceChangeListener(this)
            
            // Set up clear data button
            findPreference<androidx.preference.Preference>("clear_data")?.setOnPreferenceClickListener {
                clearAllData()
                true
            }
            
            // Update API info display
            updateApiInfo()
        } catch (e: Exception) {
            android.util.Log.e("SettingsFragment", "Error creating preferences: ${e.message}", e)
            android.widget.Toast.makeText(requireContext(), "Error loading settings", android.widget.Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun updateApiInfo() {
        try {
            val prefs = preferenceManager.sharedPreferences
            val baseUrl = prefs?.getString("api_base_url", "https://tbsg.temenos.com/api/v1.0") ?: "https://tbsg.temenos.com/api/v1.0"
            val timeout = prefs?.getInt("api_timeout", 30) ?: 30
            
            findPreference<androidx.preference.Preference>("api_info")?.summary = 
                "Base URL: $baseUrl\nTimeout: ${timeout}s"
        } catch (e: Exception) {
            android.util.Log.e("SettingsFragment", "Error updating API info: ${e.message}", e)
        }
    }
    
    override fun onSharedPreferenceChanged(sharedPreferences: SharedPreferences?, key: String?) {
        when (key) {
            "dark_mode" -> {
                val isDarkMode = sharedPreferences?.getBoolean("dark_mode", false) ?: false
                AppCompatDelegate.setDefaultNightMode(
                    if (isDarkMode) AppCompatDelegate.MODE_NIGHT_YES 
                    else AppCompatDelegate.MODE_NIGHT_NO
                )
            }
            "api_base_url", "api_timeout" -> {
                updateApiInfo()
            }
        }
    }
    
    private fun clearAllData() {
        try {
            CoroutineScope(Dispatchers.IO).launch {
                try {
                    val database = ConversationDatabase.getDatabase(requireContext())
                    database.conversationDao().deleteAllConversations()
                    
                    requireActivity().runOnUiThread {
                        Toast.makeText(requireContext(), "All conversation data cleared", Toast.LENGTH_SHORT).show()
                    }
                } catch (e: Exception) {
                    android.util.Log.e("SettingsFragment", "Error clearing data: ${e.message}", e)
                    requireActivity().runOnUiThread {
                        Toast.makeText(requireContext(), "Error clearing data: ${e.message}", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        } catch (e: Exception) {
            android.util.Log.e("SettingsFragment", "Error starting clear data: ${e.message}", e)
            Toast.makeText(requireContext(), "Error clearing data", Toast.LENGTH_SHORT).show()
        }
    }
    
    override fun onDestroy() {
        super.onDestroy()
        preferenceManager.sharedPreferences?.unregisterOnSharedPreferenceChangeListener(this)
    }
} 