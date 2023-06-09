package com.example.cankayachatbotapp

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.cankayachatbotapp.databinding.RowBinding

class Adapter(var item: List<Message>) : RecyclerView.Adapter<Adapter.ViewHolder>() {


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = RowBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val currentItem = item[position]

        holder.binding.tvUserInput.text = currentItem.userInput
        holder.binding.tvReceivedText.text = currentItem.response
        holder.binding.llRow.visibility =
            if (currentItem.userInput.isNotEmpty()) View.VISIBLE else View.GONE
        holder.binding.llImages.visibility =
            if (currentItem.userInput.isNotEmpty()) View.VISIBLE else View.GONE
    }

    override fun getItemCount(): Int {
        return item.size
    }


    class ViewHolder(val binding: RowBinding) : RecyclerView.ViewHolder(binding.root) {


    }

}

