package com.example.cankayachatbotapp

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.cankayachatbotapp.databinding.ActivityMainBinding
import com.example.cankayachatbotapp.databinding.RowBinding
import java.io.*

class MainActivity : AppCompatActivity() {

    private lateinit var gpt3Api: GPT3Api
    private lateinit var binding: ActivityMainBinding
    private lateinit var rowBinding: RowBinding
    private lateinit var adapter: Adapter
    private lateinit var fileOutputStream: FileOutputStream

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        fileOutputStream = openFileOutput("test.txt", Context.MODE_APPEND)
        binding = ActivityMainBinding.inflate(layoutInflater)
        rowBinding = RowBinding.inflate(layoutInflater, null, false)

        binding.rvMain.layoutManager = LinearLayoutManager(this)
        adapter = Adapter(emptyList()) { userInput, response, check ->
            writeToTextFile(userInput, response, check)
        }
        binding.rvMain.adapter = adapter

        val view = binding.root
        setContentView(view)



        gpt3Api = GPT3Api()

        appendToChat("", "Merhaba Hoşgeldiniz! size nasıl yardımcı olabilirim.")

        binding.buttonSend.setOnClickListener {
            val userInput = binding.etUserInput.text.toString().trim()

            if (userInput.isNotEmpty()) {
                binding.etUserInput.text.clear()
                appendToChat(userInput, "")
                getGPT3Response(userInput)
            }
        }

    }

    private fun getGPT3Response(inputText: String) {
        gpt3Api.getGPT3Response(inputText) { response ->
            runOnUiThread {
                if (response.isNotEmpty()) {
                    appendToChat(inputText, response)
                }
            }
        }
    }

    private fun appendToChat(userInput: String, response: String) {

        if (response.contains("?")) {
            val newItem = Message(userInput, "ne dediğinizi anlamadım!")
            val newList = adapter.item.toMutableList()
            newList.add(newItem)
            adapter.item = newList
            adapter.notifyDataSetChanged()
        } else if (response == "") {

        }else{
            val newItem = Message(userInput, response)
            val newList = adapter.item.toMutableList()
            newList.add(newItem)
            adapter.item = newList
            adapter.notifyDataSetChanged()
        }
    }

    private fun writeToTextFile(userInput: String, response: String, check: Boolean) {
        val blank = "\n\n"
        val blank2 = ", "
        val userInputInfo = "UserInput==> "
        val ResponseInfo = "Response==> "

        fileOutputStream.write(userInputInfo.toByteArray())
        fileOutputStream.write(userInput.toByteArray())
        fileOutputStream.write(blank2.toByteArray())
        fileOutputStream.write(ResponseInfo.toByteArray())
        fileOutputStream.write(response.toByteArray())
        fileOutputStream.write(blank2.toByteArray())
        fileOutputStream.write(check.toString().toByteArray())
        fileOutputStream.write(blank.toByteArray())
    }


}

