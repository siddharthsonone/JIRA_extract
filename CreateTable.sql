SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[JIRA_Dump](
	[TICKET ID] [nvarchar](255) NULL,
	[Summary] [nvarchar](255) NULL,
	[PMS] [nvarchar](255) NULL,
	[Submitter] [nvarchar](255) NULL,
	[DateTime] [nvarchar](255) NULL,
	[Status From] [nvarchar](255) NULL,
	[Status To] [nvarchar](255) NULL,
	[Quantity] [nvarchar](255) NULL,
	[Zocdoc ProviderID] [nvarchar](255) NULL,
	[Due Date] [nvarchar](255) NULL,
	[Time Spent] [nvarchar](255) NULL,
	[MISC1] [nvarchar](255) NULL,
	[MISC2] [nvarchar](255) NULL,
	[MISC3] [nvarchar](255) NULL,
	[MISC4] [nvarchar](255) NULL,
	[Assignee] [nvarchar](255) NULL
) ON [PRIMARY]

GO


