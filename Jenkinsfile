
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/python -m py_compile app.py
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    .venv/bin/python - <<'PY'
import unittest
from app import app

class FlaskTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        response = self.client.get('/hello?name=Test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, Test!', response.data)

    def test_default(self):
        response = self.client.get('/hello')
        self.assertIn(b'Hello, Usuario!', response.data)

    def test_xss(self):
        response = self.client.get(
            '/hello?name=<script>alert(1)</script>'
        )
        self.assertNotIn(b'<script>', response.data)

unittest.main()
PY
                '''
            }
        }

        stage('Generate Documentation') {
            steps {
                sh 'doxygen Doxyfile'
                archiveArtifacts artifacts: 'docs/html/**',
                                 allowEmptyArchive: false
            }
        }

        stage('Version Control') {
            steps {
                sh '''
                    git rev-parse HEAD > documentation-commit.txt
                    git status --short > documentation-status.txt
                '''
                archiveArtifacts artifacts: 'documentation-*.txt'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    mkdir -p deploy
                    cp app.py requirements.txt deploy/
                    cp -r docs/html deploy/documentation
                '''
                archiveArtifacts artifacts: 'deploy/**'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completado correctamente.'
        }
        failure {
            echo 'El pipeline ha fallado. Revisar los registros.'
        }
    }
}
