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
    echo "Waiting 15 seconds for SonarQube to process results..."
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
        echo "❌ Quality gate check: FAILED (${env.BLOCKER_COUNT} blockers found)"
      } else {
        env.HAS_BLOCKERS = 'false'
        echo "✅ Quality gate check: PASSED (no blockers)"
      }
    }
  }
  
  stage('Hadoop MapReduce Job') {
    script {
      if (env.HAS_BLOCKERS == 'false') {
        echo "✅ No blockers detected - executing Hadoop job"
        
        def repoUrl = 'https://github.com/MichaelRHLee01/python-code-disasters.git'
        def podName = sh(script: "/var/jenkins_home/kubectl get pod -n jenkins -l app=jenkins -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()        
        try {
          sh """
            kubectl exec -n jenkins ${podName} -c gcloud-sidecar -- gcloud dataproc jobs submit pyspark \
              gs://cmu-course-final-hadoop-scripts/line_counter.py \
              --cluster=hadoop-cluster \
              --region=us-central1 \
              --project=cmu-course-final \
              -- ${repoUrl}
          """
          
          echo "✅ Hadoop job completed successfully"
          
          def results = sh(
            script: "kubectl exec -n jenkins ${podName} -c gcloud-sidecar -- gsutil cat gs://cmu-course-final-hadoop-output/line-counts-python-code-disasters/part-* 2>/dev/null | head -20 || echo 'No results yet'",
            returnStdout: true
          ).trim()
          
          echo "\n========== HADOOP JOB RESULTS =========="
          echo results
          echo "========================================"
          
        } catch (Exception e) {
          echo "⚠️ Hadoop job failed: ${e.message}"
          currentBuild.result = 'UNSTABLE'
        }
      } else {
        echo "🚫 BLOCKERS FOUND (${env.BLOCKER_COUNT}) - Hadoop job SKIPPED"
        echo "View issues at: http://34.30.30.30:9000/project/issues?id=python-code-disasters&resolved=false&severities=BLOCKER"
      }
    }
  }
}