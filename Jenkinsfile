node {
  environment {
    PATH = "$WORKSPACE/bin:$PATH"
  }

  stage('SCM') {
    checkout scm
  }

  stage('Install jq') {
    sh '''
      mkdir -p $WORKSPACE/bin
      if [ ! -f $WORKSPACE/bin/jq ]; then
        echo "Installing jq to workspace bin..."
        curl -sLo $WORKSPACE/bin/jq https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64
        chmod +x $WORKSPACE/bin/jq
      else
        echo "jq already exists in workspace"
      fi
    '''
  }

  stage('SonarQube Analysis') {
    def scannerHome = tool 'SonarQubeScanner'
    withSonarQubeEnv('SonarQube') {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }

  stage('Quality Gate') {
    script {
      echo "Polling SonarQube quality gate..."

      def status = "PENDING"
      for (int i = 0; i < 12; i++) {
        status = sh(
          script: "curl -s -u admin:!Sonarqube123 'http://34.30.30.30:9000/api/qualitygates/project_status?projectKey=python-code-disasters' | jq -r '.projectStatus.status'",
          returnStdout: true
        ).trim()

        if (status != "PENDING") {
          break
        }

        sleep 10
      }

      env.QUALITY_GATE_STATUS = status
      echo "Quality gate result: ${status}"

      if (status != "OK") {
        currentBuild.result = 'FAILURE'
      }
    }
  }

  stage('Check Blockers') {
    script {
      def sonarUrl = 'http://34.30.30.30:9000'
      def projectKey = 'python-code-disasters'

      sleep(time: 10, unit: 'SECONDS')

      def blockerCount = sh(
        script: """
          curl -s -u admin:!Sonarqube123 '${sonarUrl}/api/issues/search?componentKeys=${projectKey}&severities=BLOCKER&resolved=false' \
          | grep -o '"total":[0-9]*' | head -n1 | cut -d':' -f2
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
        def podName = sh(script: "kubectl get pod -n jenkins -l app=jenkins -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()

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
