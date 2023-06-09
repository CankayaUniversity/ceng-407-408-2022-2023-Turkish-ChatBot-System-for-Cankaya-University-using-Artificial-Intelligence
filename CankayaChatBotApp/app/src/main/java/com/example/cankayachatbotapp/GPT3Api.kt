package com.example.cankayachatbotapp

import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class GPT3Api {
    private val client = OkHttpClient()
    private val apiKey = "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"
    private val model = "davinci:ft-personal-2023-06-04-20-22-24"

    fun getGPT3Response(inputText: String, callback: (String) -> Unit) {
        val url = "https://api.openai.com/v1/engines/$model/completions"

        val requestBody = JSONObject()
            .put("prompt", inputText)
            .put("max_tokens", 150)
            .put("temperature", 0.0)
            .put("top_p", 1.0)
            .put("frequency_penalty", 0.0)
            .put("presence_penalty", 0.0)
            .put("stop", JSONArray().put("."))

        val request = Request.Builder()
            .url(url)
            .header("Authorization", "Bearer $apiKey")
            .header("Content-Type", "application/json")
            .post(
                RequestBody.create(
                    "application/json".toMediaTypeOrNull(),
                    requestBody.toString()
                )
            )
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                callback.invoke("Error: ${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                val responseText = response.body?.string()
                val responseObject = JSONObject(responseText)

                val choices = responseObject.getJSONArray("choices")
                if (choices.length() > 0) {
                    val firstChoice = choices.getJSONObject(0)
                    val text = firstChoice.getString("text")
                    callback.invoke(text)
                } else {
                    callback.invoke("No response received.")
                }
            }
        })
    }
}
