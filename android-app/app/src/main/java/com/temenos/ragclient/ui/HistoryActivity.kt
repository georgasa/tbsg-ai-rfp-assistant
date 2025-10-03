package com.temenos.ragclient.ui

import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.SearchView
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.temenos.ragclient.R
import com.temenos.ragclient.data.Conversation
import com.temenos.ragclient.data.ConversationDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class HistoryActivity : AppCompatActivity() {
    private lateinit var adapter: ConversationAdapter
    private lateinit var database: ConversationDatabase
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_history)
        
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        title = "Conversation History"
        
        database = ConversationDatabase.getDatabase(this)
        
        setupRecyclerView()
        loadConversations()
    }
    
    private fun setupRecyclerView() {
        adapter = ConversationAdapter { conversation ->
            // Handle conversation click - could open detail view
            showConversationDetail(conversation)
        }
        
        findViewById<androidx.recyclerview.widget.RecyclerView>(R.id.recyclerView).apply {
            layoutManager = LinearLayoutManager(this@HistoryActivity)
            adapter = this@HistoryActivity.adapter
        }
    }
    
    private fun loadConversations() {
        lifecycleScope.launch {
            val conversations = withContext(Dispatchers.IO) {
                database.conversationDao().getAllConversations()
            }
            adapter.submitList(conversations)
            updateEmptyState(conversations.isEmpty())
        }
    }
    
    private fun searchConversations(query: String) {
        lifecycleScope.launch {
            val conversations = withContext(Dispatchers.IO) {
                if (query.isBlank()) {
                    database.conversationDao().getAllConversations()
                } else {
                    database.conversationDao().searchConversations(query)
                }
            }
            adapter.submitList(conversations)
            updateEmptyState(conversations.isEmpty())
        }
    }
    
    private fun updateEmptyState(isEmpty: Boolean) {
        findViewById<View>(R.id.emptyState).visibility = if (isEmpty) View.VISIBLE else View.GONE
    }
    
    private fun showConversationDetail(conversation: Conversation) {
        // Could implement a detail dialog or activity
        // For now, just show a toast
        android.widget.Toast.makeText(this, "Selected: ${conversation.question}", android.widget.Toast.LENGTH_SHORT).show()
    }
    
    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_history, menu)
        
        val searchItem = menu.findItem(R.id.action_search)
        val searchView = searchItem.actionView as SearchView
        
        searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String?): Boolean {
                searchConversations(query ?: "")
                return true
            }
            
            override fun onQueryTextChange(newText: String?): Boolean {
                searchConversations(newText ?: "")
                return true
            }
        })
        
        return true
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            android.R.id.home -> {
                finish()
                true
            }
            R.id.action_clear_history -> {
                clearAllHistory()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
    
    private fun clearAllHistory() {
        lifecycleScope.launch {
            withContext(Dispatchers.IO) {
                database.conversationDao().deleteAllConversations()
            }
            loadConversations()
            android.widget.Toast.makeText(this@HistoryActivity, "History cleared", android.widget.Toast.LENGTH_SHORT).show()
        }
    }
} 