import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mcp import McpError, GetPromptResult, stdio_server
from mcp.server import Server
from mcp.types import (Tool, ErrorData, Prompt, PromptArgument, PromptMessage,
                       TextContent, INVALID_PARAMS, INTERNAL_ERROR, METHOD_NOT_FOUND)

from pydantic import BaseModel, Field

class SendEmailModel(BaseModel):
    sender: str = Field(description="The sender's email address")
    password: str = Field(description="The sender's email password or app-specific password")
    receiver: list[str] = Field(description="The list of recipient email addresses, supports multiple recipients")
    body: str = Field(description="The main content of the email")
    subject: str = Field(description="The subject line of the email")



async def send_email(email_data: SendEmailModel):
    smtp_server = get_smtp_server(email_data.sender)
    port = email_data.port

    # 构建邮件内容
    message = MIMEMultipart()
    message["From"] = email_data.sender
    message["To"] = ", ".join(email_data.receiver)  # 将收件人列表转为逗号分隔的字符串
    message["Subject"] = email_data.subject

    message.attach(MIMEText(email_data.body, "plain"))

    try:
        # 创建 SMTP 连接
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # 向服务器发送问候命令
            server.starttls()  # 启用 TLS 加密
            server.login(email_data.sender, email_data.password)  # 使用应用专用密码
            server.sendmail(email_data.sender, email_data.receiver, message.as_string())
        return f"Email sent successfully from sender: {email_data.sender}"
    except Exception as e:
        raise ValueError(str(e))

def get_smtp_server(sender):
    domain = sender.split('@')[1]  # 域名部分
    dot_part = domain.split('.')[0]  # 结果

    return f"smtp.{dot_part}.com"

def get_lack_params(arguments: dict):
    lack_params = []

    for field_name, _ in SendEmailModel.model_fields.items():
        if field_name not in arguments:
            lack_params.append(field_name)

    return "\n".join([f"{field} is required" for field in lack_params]) if len(lack_params) != 0 else None

async def serve() -> None:
    """

    """
    server = Server("mcp-email")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="send-email",
                description="""A tool that sends emails based on the provided subject, body, sender, password, and receiver. 
                            It ensures secure and accurate email delivery while supporting multiple recipients and custom content. 
                            Ideal for automating email workflows.""",
                inputSchema=SendEmailModel.model_json_schema()
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="send-email",
                description="""A tool that sends emails based on the provided subject, body, sender, password, and receiver. 
                            It ensures secure and accurate email delivery while supporting multiple recipients and custom content. 
                            Ideal for automating email workflows.""",
                arguments=[
                    PromptArgument(
                        name="sender",
                        description="The sender's email address",
                        required=True
                    ),
                    PromptArgument(
                        name="password",
                        description="The sender's email password or app-specific password",
                        required=True
                    ),
                    PromptArgument(
                        name="receiver",
                        description="The list of recipient email addresses, supports multiple recipients",
                        required=True
                    ),
                    PromptArgument(
                        name="body",
                        description="The main content of the email",
                        required=True
                    ),
                    PromptArgument(
                        name="subject",
                        description="The subject line of the email",
                        required=True
                    )
                ]
            )
        ]

    @server.call_tool()
    async def call_tool(name, arguments: dict) -> list[TextContent]:
        if name != "send-email":
            raise McpError(ErrorData(code=METHOD_NOT_FOUND, message=""))
        try:
            args = SendEmailModel(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        try:
            email_response = await send_email(args)
            return [TextContent(type="text", text=f"Send email response: \n{email_response}")]
        except Exception as e:
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=str(e)))

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        lack_params_message = get_lack_params(arguments)
        if not arguments or not lack_params_message:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=lack_params_message))

        try:
            args = SendEmailModel(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        try:
            email_response = await send_email(args)
        except McpError as e:
            return GetPromptResult(
                description=f"Failed to send email",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=str(e)),
                    )
                ],
            )
        return GetPromptResult(
            description=f"Response of send email by {args.sender}",
            messages=[
                PromptMessage(
                    role="user", content=TextContent(type="text", text=email_response)
                )
            ],
        )

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
