from langchain_community.llms import Ollama
from plugins.memory_core import ASTRAMemoryBank # Fixed the class name!

class LocalIntelligenceCore:
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name 
        self.memory = ASTRAMemoryBank() # Boot the updated memory core
        
        print(f"[ASTRA-CORE] Initializing Offline Neural Net: {self.model_name.upper()}...")
        try:
            self.llm = Ollama(model=self.model_name)
            self.llm.invoke("Wake up.")
            print("[ASTRA-CORE] Neural Net Online and awaiting queries.")
        except Exception as e:
            print("[ERROR] Ollama engine not detected. Ensure Ollama is running locally.")
            self.llm = None

    def process_query(self, user_input):
        """Processes a query using local hardware and past memories."""
        if not self.llm:
            return "Sir, my local neural network is currently offline. Please boot Ollama."
        
        # 1. Instantly recall relevant past memories using the new search function
        past_context_results = self.memory.search_memory(user_input)
        
        # Extract the text from the search results
        past_context = ""
        if past_context_results:
            past_context = "\n".join([res["context"] for res in past_context_results])
        
        # 2. Build the master prompt with historical context
        system_prompt = (
            "You are ASTRA, an advanced AI running locally on Parth Sir's hardware. "
            "Keep responses concise, analytical, and in the tone of Iron Man's ASTRA. Do not use emojis. "
            "Use the following past memories to provide context if relevant to the current query:\n"
            f"--- PAST MEMORIES ---\n{past_context}\n---------------------\n"
            f"Current Query: {user_input}"
        )
        
        try:
            # 3. Generate the response
            response = self.llm.invoke(system_prompt).strip()
            
            # 4. Save the interaction permanently before returning using the new add_memory function
            self.memory.add_memory(f"User: {user_input} | ASTRA: {response}")
            
            return response
        except Exception as e:
            return f"Neural network error: {str(e)}"

# Instantiate the plugin globally
llm_brain = LocalIntelligenceCore()