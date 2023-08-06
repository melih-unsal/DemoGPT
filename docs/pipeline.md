# 🛠️ DemoGPT Architecture
<br/>
<br/>
<br/>
<p align="center">
<a href="https://github.com/melih-unsal/DemoGPT"><img src="https://github.com/melih-unsal/DemoGPT/blob/main/assets/architecture_transparent.png?raw=true"></a>
</p>



## How DemoGPT Works
1. **Planning**: DemoGPT starts by generating a plan from the user's instruction.
2. **Task Creation**: It then creates specific tasks from the plan and instruction.
3. **Code Snippet Generation**: These tasks are transferred into code snippets.
4. **Final Code Assembly**: The code snippets are combined into a final code, resulting in an interactive application.
5. **Refining**: All the steps including plan generation, task creation, and code snippet generation will be refined by themselves to pass to the next stage.
6. **DB Saving**: If the user approves the result then all the generated plan, tasks and code snippets are saved into the database. Thus, next time, there the similar results for the corresponding instruction will be fetched from the DB and refining process will be shorter.