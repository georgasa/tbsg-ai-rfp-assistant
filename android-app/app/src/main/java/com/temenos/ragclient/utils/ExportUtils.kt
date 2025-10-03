package com.temenos.ragclient.utils

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.core.content.FileProvider
import com.temenos.ragclient.data.Conversation
import java.io.File
import java.io.FileWriter
import java.text.SimpleDateFormat
import java.util.*

object ExportUtils {
    
    fun exportToCSV(context: Context, conversations: List<Conversation>): Uri? {
        return try {
            val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
            val fileName = "tbsg_conversations_$timestamp.csv"
            val file = File(context.cacheDir, fileName)
            
            FileWriter(file).use { writer ->
                // Write CSV header
                writer.append("Timestamp,Question,Answer,Category,Region,Model ID,Context\n")
                
                // Write data
                conversations.forEach { conversation ->
                    writer.append("\"${formatDate(conversation.timestamp)}\",")
                    writer.append("\"${escapeCsvField(conversation.question)}\",")
                    writer.append("\"${escapeCsvField(conversation.answer)}\",")
                    writer.append("\"${escapeCsvField(conversation.category)}\",")
                    writer.append("\"${escapeCsvField(conversation.region)}\",")
                    writer.append("\"${escapeCsvField(conversation.modelId)}\",")
                    writer.append("\"${escapeCsvField(conversation.context)}\"\n")
                }
            }
            
            // Create content URI for sharing
            FileProvider.getUriForFile(
                context,
                "${context.packageName}.fileprovider",
                file
            )
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
    
    fun exportToText(context: Context, conversations: List<Conversation>): Uri? {
        return try {
            val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
            val fileName = "tbsg_conversations_$timestamp.txt"
            val file = File(context.cacheDir, fileName)
            
            FileWriter(file).use { writer ->
                writer.append("TBSG AI Conversation History\n")
                writer.append("Exported on: ${formatDate(Date())}\n")
                writer.append("Total conversations: ${conversations.size}\n")
                writer.append("=" * 50 + "\n\n")
                
                conversations.forEachIndexed { index, conversation ->
                    writer.append("Conversation ${index + 1}\n")
                    writer.append("Date: ${formatDate(conversation.timestamp)}\n")
                    writer.append("Category: ${conversation.category}\n")
                    writer.append("Region: ${conversation.region}\n")
                    writer.append("Model: ${conversation.modelId}\n")
                    if (conversation.context.isNotEmpty()) {
                        writer.append("Context: ${conversation.context}\n")
                    }
                    writer.append("Question: ${conversation.question}\n")
                    writer.append("Answer: ${conversation.answer}\n")
                    writer.append("-" * 30 + "\n\n")
                }
            }
            
            FileProvider.getUriForFile(
                context,
                "${context.packageName}.fileprovider",
                file
            )
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
    
    fun shareFile(context: Context, uri: Uri, mimeType: String, title: String) {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = mimeType
            putExtra(Intent.EXTRA_STREAM, uri)
            putExtra(Intent.EXTRA_SUBJECT, title)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        
        context.startActivity(Intent.createChooser(intent, "Share via"))
    }
    
    private fun formatDate(date: Date): String {
        return SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(date)
    }
    
    private fun escapeCsvField(field: String): String {
        return field.replace("\"", "\"\"")
    }
    
    private operator fun String.times(count: Int): String {
        return repeat(count)
    }
} 