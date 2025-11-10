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
    timeout(time: 10, unit: 'MINUTES') {
      def qg = waitForQualityGate()
      env.QUALITY_GATE_STATUS = qg.status
    }
  }
  
  stage('Check Blockers') {
    script {
      // Query SonarQube API for blocker count
      def sonarUrl = 'http://34.30.30.30:9000'
      def projectKey = 'python-code-disasters'
      
      def blockerCount = sh(
        script: """
          curl -s -u admin:!Sonarqube123 '${sonarUrl}/api/issues/search?componentKeys=${projectKey}&severities=BLOCKER&resolved=false' | grep -o '"total":[0-9]*' | cut -d':' -f2
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
        
        try {
          // Submit Hadoop job
          sh """
            gcloud dataproc jobs submit pyspark \
              gs://cmu-course-final-hadoop-scripts/line_counter.py \
              --cluster=hadoop-cluster \
              --region=us-central1 \
              --project=cmu-course-final \
              -- ${repoUrl}
          """
          
          echo "✅ Hadoop job completed successfully"
          
          // Fetch results
          def results = sh(
            script: 'gsutil cat gs://cmu-course-final-hadoop-output/line-counts-python-code-disasters/part-* | head -20',
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
        echo "Fix blocker issues before deploying to production"
        echo "View issues at: http://34.30.30.30:9000/project/issues?id=python-code-disasters&resolved=false&severities=BLOCKER"
      }
    }
  }
}
