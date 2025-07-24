"""
Simplified Swagger UI integration for WeRent Backend API.
Uses modular approach with separate files for configuration, schemas, and paths.
"""

import os
from flask import Blueprint, render_template_string, jsonify

from .server_config import get_server_urls, get_api_info, get_security_schemes, get_tags
from .schemas import get_all_schemas
from .paths import get_all_paths

# Create Swagger blueprint
swagger_bp = Blueprint("swagger", __name__, url_prefix="/docs")


def get_openapi_spec():
    """Generate comprehensive OpenAPI 3.0 specification for the API."""
    return {
        "openapi": "3.0.0",
        "info": get_api_info(),
        "servers": get_server_urls(),
        "components": {
            "securitySchemes": get_security_schemes(),
            "schemas": get_all_schemas(),
        },
        "paths": get_all_paths(),
        "tags": get_tags(),
    }


@swagger_bp.route("/")
def swagger_ui():
    """Render Swagger UI page."""
    swagger_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WeRent API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui.css" />
        <style>
            html {
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }
            *, *:before, *:after {
                box-sizing: inherit;
            }
            body {
                margin: 0;
                background: #fafafa;
            }
            .swagger-ui .topbar {
                background-color: #2c3e50;
            }
            .swagger-ui .topbar .download-url-wrapper {
                display: none;
            }
            .swagger-ui .info {
                margin: 20px 0;
            }
            .swagger-ui .info .title {
                color: #2c3e50;
                font-size: 36px;
                margin: 0;
            }
            .swagger-ui .info .description {
                margin: 15px 0;
                font-size: 14px;
                line-height: 1.6;
            }
            /* Custom styles for better presentation */
            .swagger-ui .opblock.opblock-post {
                border-color: #49cc90;
            }
            .swagger-ui .opblock.opblock-get {
                border-color: #61affe;
            }
            .swagger-ui .opblock.opblock-put {
                border-color: #fca130;
            }
            .swagger-ui .opblock.opblock-delete {
                border-color: #f93e3e;
            }
            /* Admin section highlighting */
            .swagger-ui .opblock-tag[data-tag="Admin"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .swagger-ui .opblock-tag[data-tag="Admin"]:hover {
                background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                // Begin Swagger UI call region
                const ui = SwaggerUIBundle({
                    url: '/docs/swagger.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout",
                    validatorUrl: null,
                    tryItOutEnabled: true,
                    supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
                    onComplete: function() {
                        console.log("WeRent API Documentation loaded successfully");
                    },
                    requestInterceptor: function(request) {
                        // Add custom headers or modify requests if needed
                        console.log("API Request:", request.method, request.url);
                        return request;
                    },
                    responseInterceptor: function(response) {
                        // Handle responses if needed
                        console.log("API Response:", response.status, response.url);
                        return response;
                    }
                });
                // End Swagger UI call region
                
                window.ui = ui;
            };
        </script>
    </body>
    </html>
    """
    return swagger_html


@swagger_bp.route("/swagger.json")
def swagger_json():
    """Return OpenAPI specification as JSON."""
    return jsonify(get_openapi_spec())


@swagger_bp.route("/redoc")
def redoc():
    """Alternative ReDoc documentation interface."""
    redoc_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WeRent API Documentation - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body { margin: 0; padding: 0; }
        </style>
    </head>
    <body>
        <redoc spec-url='/docs/swagger.json'></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    return redoc_html


@swagger_bp.route("/health")
def docs_health():
    """Health check for documentation service."""
    return jsonify({
        "service": "WeRent API Documentation",
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "swagger_ui": "/docs/",
            "openapi_spec": "/docs/swagger.json", 
            "redoc": "/docs/redoc"
        }
    })
