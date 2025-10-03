package com.temenos.ragclient.data

import androidx.room.*
import java.util.*

@Entity(tableName = "conversations")
data class Conversation(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val question: String,
    val answer: String,
    val category: String,
    val region: String,
    val context: String,
    val timestamp: Date,
    val modelId: String
)

@Dao
interface ConversationDao {
    @Query("SELECT * FROM conversations ORDER BY timestamp DESC")
    suspend fun getAllConversations(): List<Conversation>
    
    @Query("SELECT * FROM conversations WHERE question LIKE '%' || :query || '%' OR answer LIKE '%' || :query || '%' ORDER BY timestamp DESC")
    suspend fun searchConversations(query: String): List<Conversation>
    
    @Insert
    suspend fun insertConversation(conversation: Conversation)
    
    @Delete
    suspend fun deleteConversation(conversation: Conversation)
    
    @Query("DELETE FROM conversations")
    suspend fun deleteAllConversations()
}

@Database(entities = [Conversation::class], version = 1)
@TypeConverters(Converters::class)
abstract class ConversationDatabase : RoomDatabase() {
    abstract fun conversationDao(): ConversationDao
    
    companion object {
        @Volatile
        private var INSTANCE: ConversationDatabase? = null
        
        fun getDatabase(context: android.content.Context): ConversationDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = androidx.room.Room.databaseBuilder(
                    context.applicationContext,
                    ConversationDatabase::class.java,
                    "conversation_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}

class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): Date? {
        return value?.let { Date(it) }
    }
    
    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? {
        return date?.time
    }
} 