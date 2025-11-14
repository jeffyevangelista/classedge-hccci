CREATE TABLE "users" (
	"user_id" varchar(255) PRIMARY KEY NOT NULL,
	"email" varchar(255) NOT NULL,
	"password" text NOT NULL,
	"created_at" timestamp DEFAULT now(),
	"roles" text[] DEFAULT '{"student"}' NOT NULL,
	"active" boolean DEFAULT true NOT NULL,
	"needs_password_setup" boolean DEFAULT true NOT NULL,
	"needs_onboarding" boolean DEFAULT true NOT NULL,
	CONSTRAINT "users_email_unique" UNIQUE("email")
);
