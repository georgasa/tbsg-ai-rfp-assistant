package com.temenos.ragclient.data

import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    
    @GET("health")
    suspend fun testConnection(): Response<HealthResponse>
    
    @GET("models")
    suspend fun getModels(@Query("region") region: String = "all"): Response<ModelsResponse>
    
    @POST("query")
    suspend fun queryRAG(@Body request: QueryRequest): Response<QueryResponse>
}

data class HealthResponse(
    val status: String,
    val message: String? = null,
    val timestamp: String? = null
)

data class ModelsResponse(
    val status: String,
    val data: Map<String, List<String>>,
    val metadata: Metadata? = null
)

data class QueryRequest(
    val question: String,
    val region: String,
    val RAGmodelId: String,
    val context: String = ""
)

data class QueryResponse(
    val status: String,
    val data: QueryData? = null,
    val metadata: Metadata? = null,
    val error: String? = null
)

data class QueryData(
    val question: String,
    val region: String,
    val model_id: String,
    val answer: String,
    val context_used: Boolean
)

data class Metadata(
    val api_version: String? = null,
    val timestamp: String? = null,
    val response_length: Int? = null
) 