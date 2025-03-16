# AI Speech Coach - Guidelines for Claude

## Project Inspiration and Motivation

The AI Speech Coach is inspired by the critical importance of articulate communication in personal and professional success. As highlighted in our reference material:

> "Your success is dependent on your ability to communicate... there is no more exceptional form of the capacity to be dangerous than to be articulate."

The project aims to address common speech issues that hinder effective communication:

1. **Filler Words**: The overuse of words like "um," "uh," "like," and "you know" that diminish impact
2. **Speaking Pace**: Issues with speaking too quickly or inconsistently, making it difficult for listeners to follow
3. **Unclear Structure**: Lack of logical flow in speech that confuses the audience
4. **Limited Vocabulary**: Repetitive word usage that makes speech monotonous
5. **Hesitation Patterns**: Pauses and uncertainty that undermine confidence and authority

Our vision is to create an AI coach that helps users become more articulate by:
- Analyzing their natural speech patterns from OMI device conversations
- Providing end-of-day reports with specific improvement suggestions
- Tracking progress over time with measurable metrics
- Offering personalized exercises for speech improvement

As the source material notes, becoming articulate is about "feeling your way along to see what word was appropriate for what moment" and learning to "craft your words carefully." Our AI coach will help users develop this skill systematically.

## Project Commands
- Build: TBD - To be updated once build system is established
- Test: TBD - To be updated once test framework is implemented
- Lint: TBD - To be updated once linting tools are configured

## Code Style Guidelines
- **Naming**: Use descriptive names - camelCase for variables/functions, PascalCase for classes
- **Formatting**: 2-space indentation, 80-character line limit
- **Imports**: Group imports by standard lib, third-party, and local modules with a blank line between
- **Error Handling**: Use try/catch blocks with specific error types, log meaningful error messages
- **Documentation**: JSDoc/docstring for functions, include param types and return values
- **Types**: Use strong typing (TypeScript/Python type hints) for all functions and variables

## Project Structure
- `/assets`: Contains media files such as images and videos
- Source code organization: TBD as project develops

## Speech Coaching Methodology

Our speech coaching methodology is based on principles extracted from expert communicators and will focus on five key areas:

### 1. Filler Word Analysis
- **Detection**: Identify instances of filler words like "um," "uh," "like," "you know"
- **Frequency Tracking**: Measure filler word frequency per minute and as percentage of total words
- **Context Analysis**: Identify patterns of when filler words are most commonly used
- **Improvement Target**: Reduce filler words by teaching strategic pausing techniques

### 2. Speech Pace Evaluation
- **Words Per Minute (WPM)**: Calculate average speaking pace
- **Pace Variation**: Measure consistency and appropriate variation in speaking pace
- **Optimal Range**: Determine ideal pace range for different conversation contexts
- **Improvement Target**: Achieve a balanced pace that enhances comprehension

### 3. Speech Structure Analysis
- **Topic Coherence**: Assess logical flow between conversation topics
- **Structural Elements**: Identify presence of clear openings, transitions, and conclusions
- **Thought Completion**: Measure how often thoughts are fully expressed versus abandoned
- **Improvement Target**: Develop more organized speech patterns with clear structure

### 4. Vocabulary Assessment
- **Word Variety**: Calculate type-token ratio (unique words divided by total words)
- **Word Choice**: Identify overused terms and suggest alternatives
- **Contextual Appropriateness**: Evaluate word selection based on conversation context
- **Improvement Target**: Expand active vocabulary and improve precision of expression

### 5. Confidence Markers
- **Hedging Language**: Detect phrases like "I think maybe," "sort of," "just"
- **Assertiveness**: Measure use of direct statements versus tentative ones
- **Pause Patterns**: Distinguish between strategic pauses and hesitation
- **Improvement Target**: Develop a more authoritative speaking style with purposeful word choice

Our AI Speech Coach will apply these metrics to daily conversation analysis, generating personalized insights and specific exercises for improvement. The PostgreSQL database will track these metrics over time, enabling the dashboard to show progress and areas needing attention.

## Dashboard Design

The AI Speech Coach dashboard will provide users with comprehensive insights into their speaking patterns through the following components:

### 1. Daily Analysis Summary
- **Speech Overview**: Total speaking time, conversation count, and participation level
- **Key Metrics Card**: Summary of the day's performance across the five core areas
- **Most Significant Findings**: Highlight of the most important improvements and issues
- **Suggested Focus Areas**: Prioritized list of areas to work on

### 2. Detailed Metrics Visualizations
- **Filler Word Tracker**: Bar chart showing frequency of different filler words
- **Pace Mapping**: Line chart displaying speaking pace throughout conversations
- **Structure Analysis**: Visual representation of speech organization patterns
- **Vocabulary Richness**: Graphs showing word variety and complexity over time
- **Confidence Index**: Composite score tracking speaking confidence

### 3. Progress Tracking
- **Historical Trends**: Line charts showing improvement across all metrics over time
- **Goal Achievement**: Visual indicators of progress toward personalized goals
- **Comparison View**: Option to compare current performance with past periods

### 4. Improvement Resources
- **Personalized Exercises**: Custom activities based on specific areas needing improvement
- **Example Showcase**: Model examples of effective communication techniques
- **Daily Challenge**: Specific focus area to practice in the next day's conversations

### 5. Conversation Insights
- **Conversation List**: Searchable list of analyzed conversations
- **Context Analysis**: Patterns of speech variation in different conversation types
- **Interaction Mapping**: Analysis of speaking patterns with different conversation partners

## Database Implementation

Our PostgreSQL database design will support the speech analysis dashboard with the following schema:

### 1. Users Table
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    device_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    settings JSONB
);
```

### 2. Conversations Table
```sql
CREATE TABLE conversations (
    conversation_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    start_timestamp TIMESTAMP NOT NULL,
    end_timestamp TIMESTAMP NOT NULL,
    conversation_context VARCHAR(100),
    participants_count INTEGER,
    total_duration_seconds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Speech Segments Table
```sql
CREATE TABLE speech_segments (
    segment_id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(conversation_id),
    user_id INTEGER REFERENCES users(user_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    text_content TEXT NOT NULL,
    is_user_speaking BOOLEAN NOT NULL,
    speaker_identification VARCHAR(50),
    duration_seconds INTEGER,
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Analysis Results Table
```sql
CREATE TABLE analysis_results (
    analysis_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    date DATE NOT NULL,
    total_speaking_time_seconds INTEGER,
    total_conversations INTEGER,
    filler_word_count INTEGER,
    filler_word_percentage DECIMAL(5,2),
    avg_words_per_minute INTEGER,
    pace_variability DECIMAL(5,2),
    vocabulary_diversity_score DECIMAL(5,2),
    clarity_score DECIMAL(5,2),
    confidence_score DECIMAL(5,2),
    overall_rating DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Improvement Suggestions Table
```sql
CREATE TABLE improvement_suggestions (
    suggestion_id SERIAL PRIMARY KEY,
    analysis_id INTEGER REFERENCES analysis_results(analysis_id),
    segment_id INTEGER REFERENCES speech_segments(segment_id),
    suggestion_type VARCHAR(50) NOT NULL,
    suggestion_text TEXT NOT NULL,
    priority_level INTEGER,
    example_text TEXT,
    improved_example TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Data will be collected daily at 7 PM from the OMI device, processed through our speech analysis pipeline, and stored in this database for access through the dashboard interface. The end-of-day analysis ensures comprehensive insights without interrupting the user's natural conversations throughout the day.

## Model Context Protocol (MCP) Guidelines

### MCP Core Concepts
- **Resources**: File-like data that can be read by clients (API responses, file contents)
- **Tools**: Functions that can be called by the LLM (with user approval)
- **Prompts**: Pre-written templates for user tasks

### MCP Server Implementation Best Practices
- **Validation**: Thoroughly validate all inputs
- **Error Handling**: Return clear, actionable error messages
- **Documentation**: Document all tools, resources, and prompts
- **Security**: Implement appropriate access controls and input sanitization
- **Performance**: Cache results when appropriate
- **Logging**: Include detailed logs for debugging
- **Testing**: Test edge cases and error conditions
- **State Management**: Handle concurrent requests properly

### MCP Architecture Components

### Core Architecture
- **Host**: LLM application (Claude Desktop, custom implementation) that initiates connections
- **Client**: Maintains 1:1 connections with servers within the host
- **Server**: Our MCP implementation that provides speech analysis tools
- **Transport Layer**: Communication mechanism between client and server (STDIO or SSE)

### Connection Lifecycle
1. **Initialization**:
   - Client sends `initialize` request with capabilities
   - Server responds with its capabilities
   - Client sends `initialized` notification
   - Normal message exchange begins
2. **Message Exchange**:
   - Request-Response patterns
   - One-way notifications
3. **Termination**:
   - Clean shutdown via `close()`
   - Transport disconnection
   - Error conditions

### Message Types
- **Requests**: Expect responses from the other side
- **Results**: Successful responses to requests
- **Errors**: Failed request indicators
- **Notifications**: One-way messages

## Python SDK Implementation with FastMCP
- **Installation**: Requires mcp>=1.2.0 (`pip install "mcp>=1.2.0"`)
- **Server Creation**: Use `FastMCP(name="ServerName", instructions="Optional instructions")` 
- **Tool Implementation**: Use `@mcp.tool()` decorator on functions
  ```python
  @mcp.tool()
  def my_tool(param1: str, param2: int) -> str:
      """Tool description (uses docstring for description)"""
      # Implementation...
      return result
  ```

### MCP Tool Concepts
- **Tool Definition**: Executable functions exposed by servers to clients (model-controlled)
- **Tool Structure**:
  ```typescript
  {
    name: string;          // Unique identifier for the tool
    description?: string;  // Human-readable description
    inputSchema: {         // JSON Schema for the tool's parameters
      type: "object",
      properties: { ... }  // Tool-specific parameters
    }
  }
  ```
- **Tool Discovery**: Clients access via `tools/list` endpoint
- **Tool Invocation**: Clients call via `tools/call` endpoint with name and arguments
- **Tool Updates**: Servers can notify clients of tool changes via `notifications/tools/list_changed`
- **Error Handling**:
  - Errors should be reported in the result object with `isError: true`
  - Include error details in the content array for LLM processing
- **Best Practices**:
  - Keep operations focused and atomic
  - Implement proper input validation
  - Use detailed descriptions with examples
  - Log usage for monitoring and debugging
- **Speech Coach Applicable Tools**:
  - `analyze-recording`: Process and analyze speech recordings
  - `detect-filler-words`: Identify and count filler words used
  - `measure-speech-pace`: Calculate words per minute and rhythm
  - `generate-improvement-plan`: Create personalized coaching plan
- **Resource Implementation**: Use `@mcp.resource(uri)` decorator
  ```python
  @mcp.resource("resource://my-resource")
  def get_resource() -> str:
      """Resource description"""
      return "Resource content"
      
  # Template resources with parameters
  @mcp.resource("resource://{param}/data")
  def get_dynamic_resource(param: str) -> str:
      return f"Dynamic resource for {param}"
  ```

### MCP Resource Concepts
- **Resource Definition**: Data that MCP servers expose to clients (application-controlled)
- **Resource Types**:
  - **Text Resources**: UTF-8 encoded text (code, logs, JSON/XML)
  - **Binary Resources**: Base64 encoded binary data (images, PDFs, audio files)
- **Resource URIs**: Identified using format `[protocol]://[host]/[path]`
- **Resource Discovery Methods**:
  - **Direct Resources**: Concrete resources listed via `resources/list` endpoint
  - **Resource Templates**: Dynamic resources using URI templates (RFC 6570)
- **Resource Updates**:
  - **List Changes**: Notify clients when resource lists change
  - **Content Changes**: Subscription system for resource content updates
- **Speech Coach Applicable Resources**:
  - `speech://user/{session_id}/metrics` - Speech metrics for a session
  - `speech://user/{session_id}/history` - Historical speech data
  - `speech://settings/thresholds` - Configuration settings for analysis
- **Prompt Implementation**: Use `@mcp.prompt()` decorator
  ```python
  @mcp.prompt()
  def analysis_prompt(data: str) -> list[dict]:
      """Analyze provided data"""
      return [
          {
              "role": "user",
              "content": f"Please analyze this data: {data}"
          }
      ]
  ```

### MCP Prompt Concepts
- **Prompt Definition**: Reusable templates that clients can surface to users (user-controlled)
- **Prompt Structure**:
  ```typescript
  {
    name: string;              // Unique identifier
    description?: string;      // Human-readable description
    arguments?: [              // Optional list of arguments
      {
        name: string;          // Argument identifier
        description?: string;  // Argument description
        required?: boolean;    // Whether argument is required
      }
    ]
  }
  ```
- **Prompt Discovery**: Clients access via `prompts/list` endpoint
- **Prompt Execution**: Clients use via `prompts/get` request with arguments
- **Dynamic Prompts**:
  - Can include embedded resource context
  - Can implement multi-step workflows
  - Can generate different content based on arguments
- **UI Integration**: Can be surfaced as slash commands, quick actions, or menu items
- **Speech Coach Applicable Prompts**:
  - `analyze-speech`: Analyze speech patterns from recordings or transcripts
  - `speech-improvement-plan`: Generate personalized speech improvement tips
  - `filler-word-reduction`: Techniques to reduce specific filler words
  - `confidence-building`: Exercises to improve speaking confidence
- **Context Usage**: Access MCP context in functions
  ```python
  @mcp.tool()
  async def tool_with_context(param: str, ctx: Context) -> str:
      # Log messages visible to client
      await ctx.info(f"Processing {param}")
      # Report progress
      await ctx.report_progress(50, 100)
      # Access other resources
      data = await ctx.read_resource("resource://some-data")
      return result
  ```
- **Type Validation**: Use Pydantic models for complex inputs
  ```python
  class UserData(BaseModel):
      name: str
      age: int
      
  @mcp.tool()
  def process_user(data: UserData) -> str:
      return f"User {data.name} is {data.age} years old"
  ```
- **Server Execution**: Run with `mcp.run(transport="stdio")` or `mcp.run(transport="sse")`

### Security and Error Handling Best Practices
- **Transport Security**:
  - Use TLS for remote connections
  - Implement authentication when needed
  - Ensure secure token handling
  - Use appropriate encryption for sensitive data
- **Message Validation**:
  - Validate all incoming inputs
  - Check message size limits
  - Verify JSON-RPC format
  - Sanitize input data to prevent injection attacks
- **Error Management**:
  - Use appropriate error codes
  - Include helpful error messages
  - Don't leak sensitive information
  - Implement proper exception handling
- **Resource Protection**:
  - Implement access controls
  - Rate limit requests
  - Monitor resource usage
  - Set appropriate timeouts
- **Network Security**:
  - Implement rate limiting
  - Handle denial of service scenarios
  - Monitor for unusual patterns
  - Use proper firewall rules
- **Authentication and Authorization**:
  - Validate client credentials
  - Implement authorization checks
  - Follow principle of least privilege
- **Debugging Security Issues**:
  - Enable detailed logging (securely)
  - Monitor connection attempts
  - Track authentication failures
  - Implement proper logging of security events

### MCP Sampling Concepts
- **Definition**: Allows servers to request LLM completions through the client
- **Flow**:
  1. Server sends `sampling/createMessage` request to client
  2. Client reviews request and can modify it
  3. Client samples from an LLM
  4. Client reviews the completion
  5. Client returns the result to the server
- **Request Format**:
  ```typescript
  {
    messages: [
      {
        role: "user" | "assistant",
        content: {
          type: "text" | "image",
          text?: string,  // For text
          data?: string,  // For images (base64 encoded)
          mimeType?: string
        }
      }
    ],
    modelPreferences?: { /* model hints and priorities */ },
    systemPrompt?: string,
    includeContext?: "none" | "thisServer" | "allServers",
    temperature?: number,
    maxTokens: number
  }
  ```
- **Human-in-the-Loop Controls**:
  - Clients show users the proposed prompts for approval
  - Clients show users the completions for review
  - Users maintain control over what the LLM sees and generates
- **Note**: Not yet supported in Claude Desktop (as of documentation)

### MCP Roots Concepts
- **Definition**: URIs that define boundaries where servers can operate
- **Purpose**:
  - Guide servers about relevant resources and locations
  - Clarify which resources are part of the workspace
  - Organize multiple resource groups simultaneously
- **Implementation**:
  1. Client declares `roots` capability during connection
  2. Client provides a list of suggested roots to the server
  3. Server respects these roots for resource access
  4. Client can notify the server when roots change
- **Example**:
  ```json
  {
    "roots": [
      {
        "uri": "file:///home/user/speech-recordings",
        "name": "Speech Recording Repository"
      },
      {
        "uri": "https://api.speech-analysis.com/v1",
        "name": "Speech Analysis API"
      }
    ]
  }
  ```
- **Best Practices**:
  - Only suggest necessary resources
  - Use clear, descriptive names
  - Handle root changes gracefully

### MCP Transport Concepts
- **Definition**: Mechanisms for communication between clients and servers
- **Message Format**: Uses JSON-RPC 2.0 as wire format with three types:
  ```typescript
  // Request format
  {
    jsonrpc: "2.0",
    id: number | string,
    method: string,
    params?: object
  }
  
  // Response format
  {
    jsonrpc: "2.0",
    id: number | string,
    result?: object,
    error?: {
      code: number,
      message: string,
      data?: unknown
    }
  }
  
  // Notification format
  {
    jsonrpc: "2.0",
    method: string,
    params?: object
  }
  ```
  1. **Requests**: Message with method, parameters, and expects a response
  2. **Responses**: Successful/error responses to requests
  3. **Notifications**: One-way messages without responses
- **Built-in Transport Types**:
  - **Stdio (Standard Input/Output)**:
    ```python
    # Server implementation
    from mcp import FastMCP
    
    mcp_server = FastMCP(name="speech-coach-server", instructions="Optional instructions")
    # Add tools, resources, and prompts
    mcp_server.run(transport="stdio")  # Default transport
    ```
    - Uses stdin/stdout for communication
    - Ideal for local processes and CLI tools
    - Simple process management
    - Recommended for command-line tools and local integrations
  - **SSE (Server-Sent Events)**:
    ```python
    # Server implementation with SSE
    from mcp import FastMCP
    
    mcp_server = FastMCP(name="speech-coach-server", instructions="Optional instructions")
    # Add tools, resources, and prompts
    mcp_server.run(transport="sse")  # Starts HTTP server
    ```
    - Uses Server-Sent Events for server-to-client communication
    - HTTP POST for client-to-server communication
    - Works with restricted networks
    - Better for web-based integrations
- **Custom Transport Implementation**:
  - Python transports must implement the Transport interface
  - Handle message parsing, sending, and receiving
  - Manage connection lifecycle events
- **Error Handling**:
  ```python
  # Example error handling pattern
  try:
      # Connection or message sending logic
  except Exception as e:
      # Log the error
      logger.error(f"Transport error: {e}")
      # Report error through appropriate channel
      if hasattr(self, 'onerror') and callable(self.onerror):
          self.onerror(Exception(f"Transport error: {e}"))
  ```
  - Connection errors
  - Message parsing errors
  - Network timeouts
  - Resource cleanup
- **Best Practices**:
  - Handle connection lifecycle properly
  - Clean up resources on connection close
  - Validate messages before sending
  - Log transport events for debugging
  - Implement appropriate timeouts
  - Use proper error handling
  - Monitor connection health

### Testing with MCP Inspector

The MCP Inspector is an interactive tool for testing and debugging MCP servers without needing a complete client implementation.

#### Installation and Usage
- Runs directly through `npx` without installation:
  ```bash
  # For Python servers
  npx @modelcontextprotocol/inspector uv run your_server.py
  
  # For PyPI packages
  npx @modelcontextprotocol/inspector uvx your-package-name
  
  # For locally developed servers
  npx @modelcontextprotocol/inspector node path/to/server/index.js
  ```

#### Key Features
- **Server Connection Pane**: Configure transport and environment
- **Resources Tab**: Explore and test available resources
- **Prompts Tab**: Test prompt templates with custom arguments
- **Tools Tab**: Execute tools with custom inputs
- **Notifications Pane**: View server logs and notifications

#### Development Workflow
1. **Initial Testing**:
   - Launch Inspector with your server
   - Verify basic connectivity
   - Test capability negotiation
2. **Iterative Development**:
   - Make changes to server code
   - Rebuild the server
   - Reconnect Inspector
   - Test affected functionality
3. **Edge Case Testing**:
   - Test with invalid inputs
   - Try missing required arguments
   - Verify error handling and responses

### Debugging MCP Servers

#### Debugging Tools
- **MCP Inspector**: Interactive debugging interface for direct server testing
- **Claude Desktop Developer Tools**: For integration testing with Claude
- **Server Logging**: For detailed error tracking and monitoring

#### Viewing Logs
```bash
# Follow logs in real-time (macOS)
tail -n 20 -F ~/Library/Logs/Claude/mcp*.log
```

#### Common Issues
- **Working Directory**: Always use absolute paths in configuration files
- **Environment Variables**: MCP servers inherit only a subset of environment variables
  ```json
  {
    "myserver": {
      "command": "mcp-server-myapp",
      "env": {
        "API_KEY": "some_key"
      }
    }
  }
  ```
- **Server Initialization Issues**: Check paths, configuration, environment
- **Connection Problems**: Verify server process, logs, protocol compatibility

#### Server-side Logging
- Log to stderr for automatic capture by host applications
- Never log to stdout (interferes with protocol operation)
- Send log messages via MCP protocol:
  ```python
  # For Context objects
  await ctx.info("Processing started")
  await ctx.error("Error occurred")
  
  # For low-level servers
  server.request_context.session.send_log_message(
    level="info",
    data="Server started successfully"
  )
  ```
  
#### Best Practices
- Use structured logging with consistent formats
- Include context, timestamps, and request IDs
- Log important events: initialization, tool calls, errors
- Sanitize sensitive data in logs
- Track performance metrics where appropriate

### Debugging Transport Issues

#### Tips for Debugging Transport Problems
1. **Enable Debug Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Monitor Message Flow**:
   - Log incoming and outgoing messages
   - Track message IDs and responses

3. **Check Connection States**:
   - Verify transport initialization
   - Check for proper connection handling
   - Monitor connection lifecycle events

4. **Validate Message Formats**:
   - Ensure JSON-RPC compliance
   - Check for malformed messages
   - Verify content encoding

5. **Test Error Scenarios**:
   - Simulate connection failures
   - Test timeout handling
   - Check recovery mechanisms

6. **Common Transport Issues**:
   - Stdio: Check process environment and I/O redirection
   - SSE: Verify HTTP server setup and client request handling
   - General: Check for proper message serialization/deserialization

7. **Troubleshooting Transport Problems**:
   - Check for environment variable issues
   - Verify correct transport selection
   - Look for connectivity errors
   - Monitor for request timeouts

### MCP Client Integration
- Configure Claude Desktop in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "server-name": {
        "command": "uv",
        "args": [
          "--directory",
          "/absolute/path/to/server/directory",
          "run",
          "server.py"
        ]
      }
    }
  }
  ```
- For custom clients, use MCP client libraries to connect to server

This document will be updated as the project evolves and specific build/test tooling is implemented.

## OMI Integration Guidelines

### OMI Apps Overview
- **Purpose**: Develop an AI Speech Coach as an OMI App using MCP for backend functionality
- **Target Platform**: OMI mobile app and OMI DevKit devices
- **App Type**: Real-Time Transcript Processor with audio analysis capabilities

### App Types in OMI
1. **Prompt-Based Apps**:
   - Chat Prompts: Alter OMI's conversational style and knowledge base
   - Memory Prompts: Analyze conversations and extract specific information

2. **Integration Apps**:
   - Memory Creation Triggers: Process memory data when OMI creates a new memory
   - Real-Time Transcript Processors: Process conversation transcripts in real-time
   - Integration Actions: Perform actions within the OMI ecosystem
   - Real-time Audio Streaming: Process raw audio from OMI devices

### Real-Time Transcript Processing
- Receives JSON payload with recently transcribed segments
- Endpoint format: `POST /your-endpoint?session_id=abc123&uid=user123`
- Payload structure:
  ```json
  [
    {
      "text": "Segment text",
      "speaker": "SPEAKER_00",
      "speakerId": 0,
      "is_user": false,
      "start": 10.0,
      "end": 20.0
    }
    // More segments...
  ]
  ```
- Must maintain session context across multiple calls
- Should implement logic to avoid redundant processing

### Audio Streaming Integration
- Streams audio bytes directly from OMI DevKit devices
- Endpoint format: `POST /your-endpoint?sample_rate=16000&uid=user123`
- Delivers raw audio bytes as octet-stream
- DevKit1 (v1.0.4+) and DevKit2 record at 16,000 Hz sample rate
- Configurable time interval for receiving audio chunks
- Can be used for real-time speech analysis and coaching

### Speech Coach Implementation Approach
1. **FastAPI or Flask Web Application**:
   - Create webhook endpoints for receiving transcripts/audio
   - Process and analyze speech patterns in real-time
   - Generate feedback and coaching based on analysis

2. **Speech Analysis Features**:
   - **Filler Word Detection**: Identify words like "um", "uh", "like", "you know"
   - **Pace Analysis**: Measure words per minute and speech rhythm
   - **Clarity Metrics**: Analyze pronunciation and articulation
   - **Speaking Confidence**: Detect hesitations and vocal confidence
   - **Vocabulary Diversity**: Measure lexical variety and suggest improvements

3. **Proactive Notifications**:
   - Implement a notification system for delivering real-time speech feedback
   - Enable follow-up reminders for coaching suggestions
   - Use prompt templates for personalized coaching messages

4. **Session Management**:
   - Track user progress across multiple sessions
   - Maintain speech pattern history for long-term improvement tracking
   - Implement buffering for collecting sufficient speech data before analysis

### OMI App Architecture Reference
Based on examining the OMI repository, our implementation should follow:

```
/ai-speech-coach/
├── Dockerfile            # Container for deploying the app
├── main.py               # Main FastAPI/Flask application
├── analyzer/             # Speech analysis modules
│   ├── filler_words.py   # Filler word detection
│   ├── pace.py           # Speech pace analysis
│   ├── clarity.py        # Pronunciation/clarity analysis
│   └── confidence.py     # Speaking confidence metrics
├── models/               # Data models
├── utils/                # Utility functions
│   ├── audio.py          # Audio processing utilities
│   └── notification.py   # Notification utilities
├── mcp/                  # MCP server implementation
│   ├── server.py         # FastMCP implementation
│   └── tools/            # Custom MCP tools
└── requirements.txt      # Dependencies
```

### Development Workflow
1. Create MCP server with speech analysis tools
2. Set up webhook endpoints for transcript/audio processing
3. Implement speech coaching logic based on transcript analysis
4. Test locally using the MCP Inspector 
5. Submit for review through the OMI mobile app

### Submission Guidelines
- App must adhere to community guidelines
- Provide clear setup instructions
- Include any authentication details if needed
- Clearly document webhook endpoints and expected data formats

### Example Implementation Patterns
1. **Message Buffer Pattern**:
   ```python
   class MessageBuffer:
       def __init__(self):
           self.buffers = {}  # session_id -> buffer data
           self.lock = threading.Lock()
           # Initialize other tracking variables
           
       def get_buffer(self, session_id):
           # Get or create buffer for session
           # Handle silence detection and cleanup
           return self.buffers[session_id]
   ```

2. **Speech Analysis Pattern**:
   ```python
   def analyze_speech(segments, history=None):
       # Extract speech patterns from segments
       filler_words = detect_filler_words(segments)
       pace = calculate_pace(segments)
       clarity = measure_clarity(segments)
       
       # Generate feedback based on analysis
       feedback = generate_feedback(filler_words, pace, clarity)
       return feedback
   ```

3. **Notification Pattern**:
   ```python
   def create_notification(feedback, uid):
       notification = {
           "notification": {
               "prompt": create_coaching_prompt(feedback),
               "params": ["user_name", "user_context"],
               "context": {...}
           }
       }
       return notification
   ```