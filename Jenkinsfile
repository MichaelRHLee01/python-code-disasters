node {
  stage('SCM') {
    checkout scm
  }
  
  stage('SonarQube Analysis') {
    def scannerHome = tool 'SonarQubeScanner';
    withSonarQubeEnv('SonarQube') {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
  
  stage('Quality Gate') {
    echo "SonarQube analysis completed"
    sleep(time: 15, unit: 'SECONDS')
  }
  
  stage('Check Blockers') {
    script {
      def sonarUrl = 'http://34.30.30.30:9000'
      def projectKey = 'python-code-disasters'
      
      def blockerCount = sh(
        script: """
          curl -s -u admin:!Sonarqube123 '${sonarUrl}/api/issues/search?componentKeys=${projectKey}&severities=BLOCKER&resolved=false' | grep -o '"total":[0-9]*' | cut -d':' -f2 | tr -d '\\n'
        """,
        returnStdout: true
      ).trim()
      
      env.BLOCKER_COUNT = blockerCount ?: '0'
      
      echo "Found ${env.BLOCKER_COUNT} blocker issues"
      
      if (env.BLOCKER_COUNT.toInteger() > 0) {
        env.HAS_BLOCKERS = 'true'
        echo "❌ FAILED (${env.BLOCKER_COUNT} blockers)"
      } else {
        env.HAS_BLOCKERS = 'false'
        echo "✅ PASSED (no blockers)"
      }
    }
  }
  
  stage('Hadoop MapReduce Job') {
    script {
      if (env.HAS_BLOCKERS == 'false') {
        echo "✅ No blockers - Executing Hadoop job"
        
        sh """
          POD_NAME=jenkins-567866744d-tghbp
          
          curl -X POST --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt -H "Authorization: Bearer \$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" "https://kubernetes.default.svc/api/v1/namespaces/jenkins/pods/\${POD_NAME}/exec?container=gcloud-sidecar&command=gcloud&command=dataproc&command=jobs&command=submit&command=pyspark&command=gs://cmu-course-final-hadoop-scripts/line_counter.py&command=--cluster%3Dhadoop-cluster&command=--region%3Dus-central1&command=--project%3Dcmu-course-final&command=--&command=https://github.com/MichaelRHLee01/python-code-disasters.git&stdin=false&stdout=true&stderr=true"
        """
        
        echo "✅ Hadoop job completed"
        
      } else {
        echo "🚫 BLOCKERS FOUND (${env.BLOCKER_COUNT}) - Hadoop job SKIPPED"
        echo "View issues at: http://34.30.30.30:9000/project/issues?id=python-code-disasters"
      }
    }
  }
}