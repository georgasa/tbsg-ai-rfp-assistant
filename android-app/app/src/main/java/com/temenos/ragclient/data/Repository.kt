package com.temenos.ragclient.data

import android.content.Context
import android.content.SharedPreferences
import androidx.preference.PreferenceManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

class Repository(private val context: Context? = null) {
    
    companion object {
        // Default configuration from shared config
        private val DEFAULT_BASE_URL = SharedConfig.API_CONFIG["base_url"] as String
        private val JWT_TOKEN = SharedConfig.API_CONFIG["jwt_token"] as String
        private val DEFAULT_TIMEOUT = SharedConfig.API_CONFIG["timeout"] as Int
    }
    
    private val apiService: ApiService by lazy {
        createApiService()
    }
    
    private fun createApiService(): ApiService {
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        
        // Get configurable settings or use defaults
        val baseUrl = getBaseUrl()
        val timeout = getTimeout()
        
        val client = OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .addInterceptor { chain ->
                val request = chain.request().newBuilder()
                    .addHeader("Authorization", "Bearer $JWT_TOKEN")
                    .addHeader("Content-Type", "application/json")
                    .build()
                chain.proceed(request)
            }
            .connectTimeout(timeout.toLong(), TimeUnit.SECONDS)
            .readTimeout(timeout.toLong(), TimeUnit.SECONDS)
            .writeTimeout(timeout.toLong(), TimeUnit.SECONDS)
            .build()
        
        return Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
    
    private fun getBaseUrl(): String {
        return if (context != null) {
            val prefs = PreferenceManager.getDefaultSharedPreferences(context)
            val configuredUrl = prefs.getString("api_base_url", DEFAULT_BASE_URL) ?: DEFAULT_BASE_URL
            // Ensure the URL ends with a slash for Retrofit
            if (!configuredUrl.endsWith("/")) "$configuredUrl/" else configuredUrl
        } else {
            // Ensure the URL ends with a slash for Retrofit
            if (!DEFAULT_BASE_URL.endsWith("/")) "$DEFAULT_BASE_URL/" else DEFAULT_BASE_URL
        }
    }
    
    private fun getTimeout(): Int {
        return if (context != null) {
            val prefs = PreferenceManager.getDefaultSharedPreferences(context)
            prefs.getInt("api_timeout", DEFAULT_TIMEOUT)
        } else {
            DEFAULT_TIMEOUT
        }
    }
    
    suspend fun testConnection(): Result<HealthResponse> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.testConnection()
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Connection failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getModels(region: String = "all"): Result<ModelsResponse> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getModels(region)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to get models: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun queryRAG(request: QueryRequest): Result<QueryResponse> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.queryRAG(request)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Query failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
} 