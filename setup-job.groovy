import jenkins.model.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition

def jenkins = Jenkins.getInstance()

// Set root URL
def locationConfig = jenkins.model.JenkinsLocationConfiguration.get()
locationConfig.setUrl("http://localhost:8081/")
locationConfig.save()

// Create or update pipeline job
String jobName = "blue-green-deployment"
def job = jenkins.getItem(jobName)
if (job == null) {
    job = jenkins.createProject(WorkflowJob.class, jobName)
}

def pipelineScript = new File("/workspace/Jenkinsfile").text
job.setDefinition(new CpsFlowDefinition(pipelineScript, true))
job.save()

println("SUCCESS: Pipeline job '" + jobName + "' created successfully in Jenkins!")
