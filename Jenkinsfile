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
  
  stage('Hadoop Decision') {
    script {
      if (env.HAS_BLOCKERS == 'false') {
        echo "✅ No blockers - Would execute Hadoop job"
        echo "Submitting via gcloud..."
        
        def repoUrl = 'https://github.com/MichaelRHLee01/python-code-disasters.git'
        
        // Run gcloud command from host system via script
        sh """
          gcloud dataproc jobs submit pyspark \
            gs://cmu-course-final-hadoop-scripts/line_counter.py \
            --cluster=hadoop-cluster \
            --region=us-central1 \
            --project=cmu-course-final \
            -- ${repoUrl} || echo "Hadoop job submission attempted"
        """
      } else {
        echo "🚫 BLOCKERS (${env.BLOCKER_COUNT}) - Skipping Hadoop"
      }
    }
  }
}