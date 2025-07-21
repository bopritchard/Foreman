import json
import boto3
import os
from datetime import datetime, timezone

def lambda_handler(event, context):
    try:
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        if http_method == 'GET':
            if path == '/':
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'text/html',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': get_html_content()
                }
            elif path == '/favicon.ico':
                # Return a simple 1x1 transparent PNG favicon
                favicon_data = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'image/png',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': favicon_data,
                    'isBase64Encoded': True
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'text/html',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': '<html><body><h1>404 - Not Found</h1></body></html>'
                }
        elif http_method == 'POST':
            query_params = event.get('queryStringParameters', {})
            if query_params is None:
                query_params = {}
            
            if event.get('path') == '/check-status' or query_params.get('action') == 'check-status':
                return handle_enhanced_status_check(event)
            elif query_params.get('action') == 'glue-upload':
                return handle_glue_upload(event)
            else:
                return handle_upload(event)
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def get_html_content():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Foreman Pipeline</title>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📊</text></svg>">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #13221C 0%, #408169 100%);
                min-height: 100vh;
            }
            .container {
                background: rgba(255, 255, 255, 0.98);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(19, 34, 28, 0.2);
                backdrop-filter: blur(10px);
            }
            h1 {
                color: #01AE66;
                text-align: center;
                margin-bottom: 30px;
                font-weight: 600;
            }
            .upload-area {
                border: 2px dashed #408169;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                transition: all 0.3s;
                background: rgba(255, 255, 255, 0.9);
            }
            .upload-area:hover {
                border-color: #01AE66;
                background: rgba(255, 255, 255, 0.95);
            }
            .upload-area.dragover {
                border-color: #01AE66;
                background-color: rgba(1, 174, 102, 0.1);
            }
            .file-input {
                display: none;
            }
            .upload-btn {
                background: #01AE66;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.3s;
                font-weight: 500;
            }
            .upload-btn:hover {
                background: #408169;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(1, 174, 102, 0.3);
            }
            .upload-btn:disabled {
                background: #13221C;
                cursor: not-allowed;
                opacity: 0.6;
            }
            .progress-container {
                margin-top: 30px;
                display: none;
            }
            .progress-bar {
                width: 100%;
                height: 20px;
                background-color: rgba(19, 34, 28, 0.1);
                border-radius: 10px;
                overflow: hidden;
                margin-bottom: 10px;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #01AE66, #408169);
                width: 0%;
                transition: width 0.3s ease;
            }
            .progress-fill.running {
                background: linear-gradient(90deg, #01AE66, #408169);
                animation: progressPulse 2s infinite;
            }
            @keyframes progressPulse {
                0%, 100% { 
                    background: linear-gradient(90deg, #01AE66, #408169);
                }
                50% { 
                    background: linear-gradient(90deg, #408169, #01AE66);
                }
            }
            .status-text {
                text-align: center;
                margin-bottom: 20px;
                font-size: 16px;
                transition: color 0.3s ease;
                color: #13221C;
            }
            .status-text.running {
                color: #01AE66;
                animation: blink 1.5s infinite;
            }
            @keyframes blink {
                0%, 50% { opacity: 1; }
                51%, 100% { opacity: 0.6; }
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .metric-card {
                background: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                border: 1px solid rgba(1, 174, 102, 0.2);
            }
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                color: #01AE66;
                margin-bottom: 5px;
            }
            .metric-label {
                color: #13221C;
                font-size: 14px;
            }
            .status-updates {
                margin-top: 20px;
                max-height: 200px;
                overflow-y: auto;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
            }
            .status-update {
                padding: 10px;
                margin-bottom: 8px;
                border-radius: 8px;
                font-size: 14px;
                border-left: 4px solid;
            }
            .status-update.info {
                background-color: rgba(1, 174, 102, 0.1);
                color: #01AE66;
                border-left-color: #01AE66;
            }
            .status-update.success {
                background-color: rgba(1, 174, 102, 0.15);
                color: #01AE66;
                border-left-color: #01AE66;
            }
            .status-update.warning {
                background-color: rgba(64, 129, 105, 0.1);
                color: #408169;
                border-left-color: #408169;
            }
            .status-update.error {
                background-color: rgba(19, 34, 28, 0.1);
                color: #13221C;
                border-left-color: #13221C;
            }
            .data-flow-section {
                margin-top: 40px;
                padding: 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                color: white;
            }
            .data-flow-title {
                text-align: center;
                font-size: 24px;
                margin-bottom: 30px;
                font-weight: bold;
            }
            .flow-diagram {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 30px;
            }
            .flow-step {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                min-width: 120px;
            }
            .flow-icon {
                width: 60px;
                height: 60px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                margin-bottom: 10px;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            .flow-step-title {
                font-weight: bold;
                margin-bottom: 5px;
                font-size: 14px;
            }
            .flow-step-desc {
                font-size: 12px;
                opacity: 0.9;
            }
            .flow-arrow {
                font-size: 24px;
                color: rgba(255, 255, 255, 0.7);
                margin: 0 10px;
            }
            .tech-highlight {
                background: linear-gradient(45deg, #ff6b6b, #feca57);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: bold;
            }
            .python-highlight {
                background: linear-gradient(45deg, #3776ab, #ffde57);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: bold;
            }
            .pandas-highlight {
                background: linear-gradient(45deg, #130654, #ff6b6b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: bold;
            }
            .accordion-header {
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(135deg, #01AE66 0%, #408169 100%);
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 18px;
                transition: all 0.3s ease;
                margin-top: 30px;
            }
            .accordion-header:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(1, 174, 102, 0.3);
            }
            .accordion-icon {
                transition: transform 0.3s ease;
                font-size: 20px;
            }
            .accordion-header.expanded .accordion-icon {
                transform: rotate(180deg);
            }
            .accordion-content {
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease;
                background: linear-gradient(135deg, #01AE66 0%, #408169 100%);
                border-radius: 0 0 15px 15px;
                margin-top: -10px;
                padding: 0 30px 30px 30px;
            }
            .flow-diagram {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 30px;
                padding-top: 20px;
            }
            .accordion-content.expanded {
                max-height: 1200px;
            }
            .processing-notice {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background: rgba(255, 193, 7, 0.95);
                border-top: 2px solid #ffc107;
                padding: 12px 20px;
                box-shadow: 0 -4px 15px rgba(255, 193, 7, 0.3);
                z-index: 1000;
                backdrop-filter: blur(10px);
            }
            .notice-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                cursor: pointer;
                font-weight: 700;
                color: #856404;
                font-size: 18px;
                text-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .notice-header span:first-child {
                animation: noticeBlink 2s infinite;
                font-weight: 800;
                color: #13221C;
                text-shadow: 0 2px 4px rgba(19, 34, 28, 0.3);
                text-align: center;
                flex-grow: 1;
            }
            @keyframes noticeBlink {
                0%, 50% { 
                    opacity: 1;
                    transform: scale(1);
                }
                25%, 75% { 
                    opacity: 0.8;
                    transform: scale(1.02);
                }
            }
            .notice-icon {
                transition: transform 0.3s ease;
                font-size: 18px;
            }
            .notice-icon.expanded {
                transform: rotate(180deg);
            }
            .notice-content {
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease;
                color: #856404;
                font-size: 14px;
                line-height: 1.5;
                margin-top: 8px;
            }
            .notice-content.expanded {
                max-height: 300px;
            }
            .notice-content p {
                margin: 8px 0;
            }
            .notice-content strong {
                color: #01AE66;
            }
            .notice-content em {
                font-style: italic;
                color: #408169;
            }
            .flow-step {
                position: relative;
                cursor: pointer;
                transition: transform 0.2s ease;
            }
            .flow-step:hover {
                transform: scale(1.05);
            }
            .tooltip {
                position: absolute;
                background: rgba(0, 0, 0, 0.9);
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 12px;
                max-width: 250px;
                white-space: normal;
                z-index: 9999;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s ease, visibility 0.3s ease;
                pointer-events: none;
            }
            .tooltip.below {
                top: 100%;
                left: 50%;
                transform: translateX(-50%);
                margin-top: 10px;
            }
            .tooltip.right {
                left: 70%;
                top: 0;
                margin-left: 5px;
            }
            .tooltip.above {
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                margin-bottom: 10px;
            }
            .flow-step:hover .tooltip {
                opacity: 1;
                visibility: visible;
            }
            .tooltip::after {
                content: '';
                position: absolute;
                top: 100%;
                left: 50%;
                transform: translateX(-50%);
                border: 6px solid transparent;
                border-top-color: rgba(0, 0, 0, 0.9);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Foreman Pipeline</h1>
            
            <div class="upload-area" id="uploadArea">
                <p>📁 Drag and drop your CSV file here, or click to select</p>
                <input type="file" id="fileInput" class="file-input" accept=".csv">
                <button class="upload-btn" onclick="document.getElementById('fileInput').click()">Choose File</button>
            </div>
            
            <div class="progress-container" id="progressContainer">
                <div class="status-text" id="statusText">🔄 Starting upload...</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="metrics-grid" id="metricsGrid"></div>
                <div class="status-updates" id="statusUpdates"></div>
            </div>
            
            <div class="accordion-header" onclick="toggleAccordion()">
                <span>🔄 Data Processing Pipeline</span>
                <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content" id="accordionContent">
                <div class="flow-diagram">
                    <div class="flow-step">
                        <div class="flow-icon">📁</div>
                        <div class="flow-step-title">CSV Upload</div>
                        <div class="flow-step-desc">Drag & drop your file</div>
                        <div class="tooltip right">Simple file upload interface for CSV files. Supports drag & drop for easy user experience.</div>
                    </div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-step">
                        <div class="flow-icon">
                            <svg width="32" height="32" viewBox="0 0 32 32">
                                <defs>
                                    <linearGradient id="s3Gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                        <stop offset="0%" style="stop-color:#28a745;stop-opacity:1" />
                                        <stop offset="100%" style="stop-color:#1e7e34;stop-opacity:1" />
                                    </linearGradient>
                                </defs>
                                <rect width="32" height="32" fill="url(#s3Gradient)"/>
                                <!-- Bucket outline -->
                                <ellipse cx="16" cy="10" rx="8" ry="3" fill="none" stroke="white" stroke-width="1.5"/>
                                <line x1="8" y1="10" x2="8" y2="22" stroke="white" stroke-width="1.5"/>
                                <line x1="24" y1="10" x2="24" y2="22" stroke="white" stroke-width="1.5"/>
                                <path d="M8 22 Q16 24 24 22" fill="none" stroke="white" stroke-width="1.5"/>
                                <!-- Handle -->
                                <circle cx="10" cy="12" r="1" fill="white"/>
                                <path d="M10 12 Q12 10 14 12" fill="none" stroke="white" stroke-width="1.5"/>
                            </svg>
                        </div>
                        <div class="flow-step-title">AWS S3</div>
                        <div class="flow-step-desc">Secure file storage</div>
                        <div class="tooltip right">Highly durable and scalable object storage. Perfect for temporary file storage before processing.</div>
                    </div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-step">
                        <div class="flow-icon">
                            <svg width="32" height="32" viewBox="0 0 32 32">
                                <rect width="32" height="32" fill="#6f42c1"/>
                                <!-- Input squares -->
                                <rect x="8" y="4" width="2" height="2" fill="white"/>
                                <rect x="12" y="6" width="2" height="2" fill="white"/>
                                <rect x="16" y="4" width="2" height="2" fill="white"/>
                                <!-- Funnel outline -->
                                <path d="M6 8 L26 8 L22 16 L22 20 L10 20 L10 16 Z" fill="none" stroke="white" stroke-width="1.5"/>
                                <!-- Output arrow -->
                                <path d="M14 22 L18 22 L16 26 Z" fill="white"/>
                            </svg>
                        </div>
                        <div class="flow-step-title">AWS Glue</div>
                        <div class="flow-step-desc">Serverless ETL</div>
                        <div class="tooltip right">⚠️ DEMO ONLY: Glue is slower & more expensive than Lambda for simple CSV processing. Production would use Lambda with pandas for faster, cheaper processing. Glue is better for complex transformations.</div>
                    </div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-step">
                        <div class="flow-icon">
                            <svg width="32" height="32" viewBox="0 0 32 32">
                                <defs>
                                    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                                        <feDropShadow dx="1" dy="1" stdDeviation="1" flood-color="#00000020"/>
                                    </filter>
                                </defs>
                                <g filter="url(#shadow)">
                                    <!-- Blue snake -->
                                    <path d="M8 8 C8 4, 12 4, 16 4 C20 4, 24 4, 24 8 C24 12, 20 12, 16 12 C12 12, 8 12, 8 16 C8 20, 12 20, 16 20 C20 20, 24 20, 24 24 C24 28, 20 28, 16 28 C12 28, 8 28, 8 24" 
                                          fill="#4B8BBE" stroke="#4B8BBE" stroke-width="0.5"/>
                                    <!-- Yellow snake -->
                                    <path d="M24 8 C24 4, 20 4, 16 4 C12 4, 8 4, 8 8 C8 12, 12 12, 16 12 C20 12, 24 12, 24 16 C24 20, 20 20, 16 20 C12 20, 8 20, 8 24 C8 28, 12 28, 16 28 C20 28, 24 28, 24 24" 
                                          fill="#FFD43B" stroke="#FFD43B" stroke-width="0.5"/>
                                    <!-- Eyes -->
                                    <circle cx="10" cy="10" r="1" fill="white"/>
                                    <circle cx="22" cy="22" r="1" fill="white"/>
                                </g>
                            </svg>
                        </div>
                        <div class="flow-step-title">Python</div>
                        <div class="flow-step-desc">Data processing</div>
                        <div class="tooltip right">Python provides excellent data processing capabilities with rich ecosystem. Perfect for CSV manipulation and validation.</div>
                    </div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-step">
                        <div class="flow-icon">
                            <svg width="32" height="32" viewBox="0 0 32 32">
                                <rect x="2" y="2" width="4" height="28" fill="#1f4e79"/>
                                <rect x="8" y="8" width="3" height="8" fill="#1f4e79"/>
                                <rect x="8" y="18" width="3" height="8" fill="#1f4e79"/>
                                <rect x="9" y="16" width="1" height="2" fill="#ffde57"/>
                                <rect x="13" y="8" width="3" height="8" fill="#1f4e79"/>
                                <rect x="13" y="18" width="3" height="8" fill="#1f4e79"/>
                                <rect x="14" y="16" width="1" height="2" fill="#ff6b6b"/>
                                <rect x="18" y="2" width="4" height="28" fill="#1f4e79"/>
                            </svg>
                        </div>
                        <div class="flow-step-title">Pandas</div>
                        <div class="flow-step-desc">Data manipulation</div>
                        <div class="tooltip right">🐼 Pandas excels at CSV processing with powerful data manipulation. Production would use pandas in Lambda for faster processing than Glue.</div>
                    </div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-step">
                        <div class="flow-icon">
                            <svg width="32" height="32" viewBox="0 0 32 32">
                                <rect width="32" height="32" fill="#1f4e79"/>
                                <!-- Database cylinders -->
                                <rect x="6" y="8" width="8" height="3" rx="1.5" fill="white"/>
                                <circle cx="8" cy="9.5" r="0.5" fill="#1f4e79"/>
                                <circle cx="10" cy="9.5" r="0.5" fill="#1f4e79"/>
                                <rect x="6" y="12" width="8" height="3" rx="1.5" fill="white"/>
                                <circle cx="8" cy="13.5" r="0.5" fill="#1f4e79"/>
                                <circle cx="10" cy="13.5" r="0.5" fill="#1f4e79"/>
                                <rect x="6" y="16" width="8" height="3" rx="1.5" fill="white"/>
                                <circle cx="8" cy="17.5" r="0.5" fill="#1f4e79"/>
                                <circle cx="10" cy="17.5" r="0.5" fill="#1f4e79"/>
                                <!-- Lightning bolt -->
                                <path d="M18 6 L22 12 L20 12 L24 18 L22 18 L18 26 L20 18 L18 18 Z" fill="white"/>
                            </svg>
                        </div>
                        <div class="flow-step-title">DynamoDB</div>
                        <div class="flow-step-desc">NoSQL database</div>
                        <div class="tooltip right">⚠️ DEMO ONLY: DynamoDB is a simple NoSQL database. Production would use PostgreSQL, Snowflake, or Redshift for scalable analytics.</div>
                    </div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-step">
                        <div class="flow-icon">📊</div>
                        <div class="flow-step-title">Real-time UI</div>
                        <div class="flow-step-desc">Progress tracking</div>
                        <div class="tooltip right">Real-time progress tracking with live updates. Shows processing status, metrics, and completion status.</div>
                    </div>
                </div>
                <div style="text-align: center; font-size: 14px; opacity: 0.9; padding: 20px;">
                    AWS Serverless Architecture • Python • Pandas • Real-time Processing
                </div>
            </div>
        </div>

        <div class="processing-notice" id="processingNotice">
            <div class="notice-header" onclick="toggleNotice()">
                <span>Why is this taking so long?</span>
                <span class="notice-icon" id="noticeIcon">▼</span>
            </div>
            <div class="notice-content" id="noticeContent">
                <p>
                    Right now, you're watching a heavyweight team—<strong>Pandas + AWS Glue</strong>—analyze your data like it owes them money.
                </p>
                <p>
                    Sure, this file is tiny. And yes, it's finishing in under a minute.
                </p>
                <p>
                    But when your datasets grow teeth—<em>wide, nested, messy, millions-of-rows teeth</em>—this same rigor is what keeps things sane.
                </p>
                <p>So we're not slow. We're just <strong>ready for your data's villain arc</strong>.</p>
            </div>
        </div>

        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const progressContainer = document.getElementById('progressContainer');
            const statusText = document.getElementById('statusText');
            const progressFill = document.getElementById('progressFill');
            const metricsGrid = document.getElementById('metricsGrid');
            const statusUpdates = document.getElementById('statusUpdates');
            
            let currentS3Key = null;
            let totalRecords = 0;
            let checkStatusInterval = null;
            
            // Drag and drop functionality
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            });
            
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFile(e.target.files[0]);
                }
            });
            
            function handleFile(file) {
                if (!file.name.toLowerCase().endsWith('.csv')) {
                    alert('Please select a CSV file');
                    return;
                }
                
                uploadFile(file);
            }
            
            async function uploadFile(file) {
                try {
                    progressContainer.style.display = 'block';
                    statusText.textContent = '📤 Uploading file...';
                    progressFill.style.width = '10%';
                    
                    const reader = new FileReader();
                    reader.onload = async function(e) {
                        const csvData = e.target.result;
                        const base64Data = btoa(csvData);
                        
                        const response = await fetch('?action=glue-upload', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                csv_data: base64Data,
                                filename: file.name
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            currentS3Key = result.filename;
                            totalRecords = result.total_records || 0;
                            statusText.textContent = '🚀 Glue job started! Monitoring progress...';
                            progressFill.style.width = '20%';
                            
                            addStatusUpdate('info', '✅ File uploaded successfully');
                            addStatusUpdate('info', `📊 Total records to process: ${totalRecords}`);
                            addStatusUpdate('info', '🔄 Starting AWS Glue processing...');
                            
                            // Start monitoring progress
                            startProgressMonitoring();
                        } else {
                            throw new Error(result.error || 'Upload failed');
                        }
                    };
                    
                    reader.readAsText(file);
                    
                } catch (error) {
                    console.error('Upload error:', error);
                    statusText.textContent = '❌ Upload failed: ' + error.message;
                    addStatusUpdate('error', '❌ Upload failed: ' + error.message);
                }
            }
            
            function startProgressMonitoring() {
                if (checkStatusInterval) {
                    clearInterval(checkStatusInterval);
                }
                
                checkStatusInterval = setInterval(async () => {
                    try {
                        const response = await fetch('?action=check-status', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                s3_key: currentS3Key
                            })
                        });
                        
                        const result = await response.json();
                        
                        updateProgress(result);
                        
                        if (result.processed) {
                            clearInterval(checkStatusInterval);
                            checkStatusInterval = null;
                        }
                        
                    } catch (error) {
                        console.error('Status check error:', error);
                        addStatusUpdate('error', '❌ Status check failed: ' + error.message);
                    }
                }, 2000); // Check every 2 seconds
            }
            
            function updateProgress(data) {
                const recordsProcessed = data.records_processed || 0;
                const totalRecordsFromData = data.total_records || 0;
                const jobStatus = data.job_status || 'UNKNOWN';
                
                // Update progress bar
                const effectiveTotalRecords = totalRecordsFromData || totalRecords;
                if (effectiveTotalRecords > 0) {
                    const progress = Math.min((recordsProcessed / effectiveTotalRecords) * 100, 100);
                    progressFill.style.width = progress + '%';
                }
                
                // Add running animation to progress bar
                if (jobStatus === 'RUNNING' || jobStatus === 'STARTING' || jobStatus === 'STOPPING') {
                    progressFill.classList.add('running');
                } else {
                    progressFill.classList.remove('running');
                }
                
                // Update status text
                if (data.processed) {
                    statusText.classList.remove('running');
                    if (data.success) {
                        statusText.textContent = '✅ Processing complete!';
                    } else {
                        statusText.textContent = '❌ Processing failed';
                    }
                } else {
                    if (jobStatus === 'RUNNING' || jobStatus === 'STARTING' || jobStatus === 'STOPPING') {
                        statusText.classList.add('running');
                        statusText.textContent = `🔄 ${jobStatus}... ${recordsProcessed}/${effectiveTotalRecords} records processed`;
                    } else {
                        statusText.classList.remove('running');
                        statusText.textContent = `⏳ ${jobStatus}... ${recordsProcessed}/${effectiveTotalRecords} records processed`;
                    }
                }
                
                // Update metrics
                updateMetrics(data);
                
                // Add status updates
                if (data.status_updates && data.status_updates.length > 0) {
                    data.status_updates.forEach(update => {
                        addStatusUpdate(update.type, update.message);
                    });
                }
            }
            
            function updateMetrics(data) {
                const metrics = [
                    { label: 'Records Processed', value: data.records_processed || 0 },
                    { label: 'Total Records', value: data.total_records || 0 },
                    { label: 'Job Status', value: data.job_status || 'UNKNOWN' },
                    { label: 'Processing Speed', value: data.job_metrics?.processing_speed || '--' },
                    { label: 'Duration', value: data.job_metrics?.duration || '--' },
                    { label: 'DPU Usage', value: data.job_metrics?.dpu_usage || '--' }
                ];
                
                metricsGrid.innerHTML = metrics.map(metric => `
                    <div class="metric-card">
                        <div class="metric-value">${metric.value}</div>
                        <div class="metric-label">${metric.label}</div>
                    </div>
                `).join('');
            }
            
            function addStatusUpdate(type, message) {
                const update = document.createElement('div');
                update.className = `status-update ${type}`;
                update.textContent = message;
                statusUpdates.appendChild(update);
                statusUpdates.scrollTop = statusUpdates.scrollHeight;
            }
            
            function toggleAccordion() {
                const header = document.querySelector('.accordion-header');
                const content = document.getElementById('accordionContent');
                
                if (content.classList.contains('expanded')) {
                    content.classList.remove('expanded');
                    header.classList.remove('expanded');
                } else {
                    content.classList.add('expanded');
                    header.classList.add('expanded');
                }
            }
            
            function toggleNotice() {
                const icon = document.getElementById('noticeIcon');
                const content = document.getElementById('noticeContent');
                
                if (content.classList.contains('expanded')) {
                    content.classList.remove('expanded');
                    icon.classList.remove('expanded');
                } else {
                    content.classList.add('expanded');
                    icon.classList.add('expanded');
                }
            }
            

            

        </script>
    </body>
    </html>
    '''

def handle_enhanced_status_check(event):
    try:
        body = event.get('body', '{}')
        if event.get('isBase64Encoded', False):
            import base64
            body = base64.b64decode(body).decode('utf-8')
        
        data = json.loads(body)
        s3_key = data.get('s3_key')
        
        if not s3_key:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Missing s3_key'})
            }
        
        response_data = {
            'processed': False,
            'job_status': 'UNKNOWN',
            'job_run_id': None,
            'job_metrics': {},
            'status_updates': [],
            'total_records': 0,
            'records_processed': 0,
            'successful_records': 0,
            'error_records': 0
        }
        
        # Check DynamoDB for processed records from this file FIRST
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table(f"foreman-{os.environ.get('ENVIRONMENT', 'dev')}-customers")
        
        # Query DynamoDB for records from this specific file
        response = table.scan(
            FilterExpression='source_file = :source_file',
            ExpressionAttributeValues={':source_file': s3_key}
        )
        
        records_processed = len(response['Items'])
        successful_records = records_processed  # Assuming all records in DynamoDB are successful
        error_records = 0  # We don't store failed records in DynamoDB currently
        
        # Try to get total_records from the upload response or estimate from CSV
        # For now, we'll use the processed count as total, but ideally we'd store this
        total_records = records_processed  # This will be updated when we store total_records from upload
        
        # Now check Glue job status
        try:
            glue = boto3.client('glue', region_name='us-east-1')
            job_name = f"foreman-{os.environ.get('ENVIRONMENT', 'dev')}-csv-processing-job"
            
            # Get the most recent job run
            response = glue.get_job_runs(JobName=job_name, MaxResults=5)
            job_status = 'UNKNOWN'
            job_run_id = None
            job_metrics = {}
            
            if response['JobRuns']:
                # Get the most recent job run
                most_recent_job = response['JobRuns'][0]  # Jobs are sorted by start time descending
                job_status = most_recent_job.get('JobRunState', 'UNKNOWN')
                job_run_id = most_recent_job.get('JobRunId', None)
                
                # Calculate actual duration from job run data
                if most_recent_job.get('StartedOn') and most_recent_job.get('CompletedOn'):
                    duration = (most_recent_job['CompletedOn'] - most_recent_job['StartedOn']).total_seconds()
                    job_metrics['duration'] = f"{duration:.1f}s"
                elif most_recent_job.get('StartedOn'):
                    # Make sure both datetimes are timezone-aware
                    now = datetime.now(timezone.utc)
                    started_on = most_recent_job['StartedOn']
                    if started_on.tzinfo is None:
                        started_on = started_on.replace(tzinfo=timezone.utc)
                    duration = (now - started_on).total_seconds()
                    job_metrics['duration'] = f"{duration:.1f}s"
                else:
                    job_metrics['duration'] = '--'
                
                # Get actual DPU usage from job run
                job_metrics['dpu_usage'] = f"{most_recent_job.get('MaxCapacity', 0)} DPU"
                job_metrics['memory_usage'] = '4GB+'
                
                # Calculate real processing speed
                if records_processed > 0 and job_metrics['duration'] != '--':
                    try:
                        duration_seconds = float(job_metrics['duration'].replace('s', ''))
                        if duration_seconds > 0:
                            speed = records_processed / duration_seconds
                            job_metrics['processing_speed'] = f"{speed:.1f} records/sec"
                        else:
                            job_metrics['processing_speed'] = '--'
                    except:
                        job_metrics['processing_speed'] = '--'
                else:
                    job_metrics['processing_speed'] = '--'
            
            response_data['job_status'] = job_status
            response_data['job_run_id'] = job_run_id
            response_data['job_metrics'] = job_metrics
            
        except Exception as e:
            response_data['status_updates'].append({
                'type': 'warning',
                'message': f'⚠️ Could not check Glue job status: {str(e)}'
            })
        
        # Determine processing status based on Glue job status and DynamoDB records
        if job_status in ['SUCCEEDED', 'STOPPED']:
            if records_processed > 0:
                status = 'processed'
                success = True
                response_data['message'] = f'✅ Processing complete! {records_processed} records processed successfully.'
            else:
                status = 'failed'
                success = False
                response_data['message'] = '❌ Job completed but no records were processed.'
        elif job_status in ['FAILED', 'ERROR', 'TIMEOUT']:
            status = 'failed'
            success = False
            response_data['message'] = f'❌ Job failed with status: {job_status}'
        elif job_status in ['RUNNING', 'STARTING', 'STOPPING']:
            status = 'processing'
            success = None
            response_data['message'] = f'🔄 Job is {job_status.lower()}... {records_processed} records processed so far.'
        else:
            status = 'unknown'
            success = None
            response_data['message'] = f'⏳ Job status: {job_status} - {records_processed} records processed so far.'
        
        response_data.update({
            'processed': status in ['processed', 'failed'],
            'success': success,
            's3_key': s3_key,
            'status': status,
            'records_processed': records_processed,
            'total_records': total_records,
            'successful_records': successful_records,
            'error_records': error_records,
            'errors': [] if success else ['File processing failed']
        })
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def handle_glue_upload(event):
    try:
        import base64
        import hashlib
        import uuid
        
        body = event.get('body', '{}')
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body).decode('utf-8')
        
        data = json.loads(body)
        csv_data = data.get('csv_data', '')
        filename = data.get('filename', f'upload_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        
        if not csv_data:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'No CSV data provided'})
            }
        
        try:
            csv_content = base64.b64decode(csv_data).decode('utf-8')
            
            # Count the actual rows in the CSV (excluding header)
            lines = csv_content.strip().split('\n')
            total_records = len(lines) - 1  # Subtract 1 for header row
            if total_records < 0:
                total_records = 0
                
        except Exception as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': f'Invalid CSV data: {str(e)}'})
            }
        
        s3 = boto3.client('s3')
        bucket_name = f'foreman-{os.environ.get("ENVIRONMENT", "dev")}-csv-uploads'
        s3_key = filename
        
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=csv_content,
            ContentType='text/csv'
        )
        
        glue = boto3.client('glue', region_name='us-east-1')
        job_name = f"foreman-{os.environ.get('ENVIRONMENT', 'dev')}-csv-processing-job"
        job_run_id = str(uuid.uuid4())
        
        try:
            response = glue.start_job_run(
                JobName=job_name
            )
            job_run_id = response['JobRunId']
        except Exception as glue_error:
            if 'ConcurrentRunsExceededException' in str(glue_error):
                job_run_id = f"pending_{job_run_id}"
            else:
                raise glue_error
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'message': 'File uploaded and Glue job started successfully',
                'filename': filename,
                'job_run_id': job_run_id,
                'total_records': total_records,
                'processing_method': 'AWS Glue with Enhanced Progress Tracking',
                'processing_details': {
                    'method': 'AWS Glue ETL Processing',
                    'description': 'Serverless ETL processing with full pandas support',
                    'features': ['Real-time progress tracking', 'Enhanced status monitoring', 'Performance metrics'],
                    'performance': 'Scalable processing with detailed progress updates'
                }
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def handle_upload(event):
    # Legacy upload handler - kept for compatibility
    return handle_glue_upload(event) 