package com.temenos.ragclient.ui

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.temenos.ragclient.R
import com.temenos.ragclient.data.Conversation
import java.text.SimpleDateFormat
import java.util.*

class ConversationAdapter(
    private val onConversationClick: (Conversation) -> Unit
) : ListAdapter<Conversation, ConversationAdapter.ConversationViewHolder>(ConversationDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ConversationViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_conversation, parent, false)
        return ConversationViewHolder(view, onConversationClick)
    }

    override fun onBindViewHolder(holder: ConversationViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class ConversationViewHolder(
        itemView: View,
        private val onConversationClick: (Conversation) -> Unit
    ) : RecyclerView.ViewHolder(itemView) {
        
        private val questionText: TextView = itemView.findViewById(R.id.questionText)
        private val answerText: TextView = itemView.findViewById(R.id.answerText)
        private val categoryText: TextView = itemView.findViewById(R.id.categoryText)
        private val timestampText: TextView = itemView.findViewById(R.id.timestampText)
        private val regionText: TextView = itemView.findViewById(R.id.regionText)
        
        private val dateFormat = SimpleDateFormat("MMM dd, yyyy HH:mm", Locale.getDefault())
        
        fun bind(conversation: Conversation) {
            questionText.text = conversation.question
            answerText.text = conversation.answer.take(100) + if (conversation.answer.length > 100) "..." else ""
            categoryText.text = conversation.category
            regionText.text = conversation.region
            timestampText.text = dateFormat.format(conversation.timestamp)
            
            itemView.setOnClickListener {
                onConversationClick(conversation)
            }
        }
    }
}

class ConversationDiffCallback : DiffUtil.ItemCallback<Conversation>() {
    override fun areItemsTheSame(oldItem: Conversation, newItem: Conversation): Boolean {
        return oldItem.id == newItem.id
    }

    override fun areContentsTheSame(oldItem: Conversation, newItem: Conversation): Boolean {
        return oldItem == newItem
    }
} 