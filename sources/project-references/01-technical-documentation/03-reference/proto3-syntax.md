# Protocol Buffers (Proto3) Quick Reference

## Overview

Protocol Buffers (protobuf) is Google's language-neutral, platform-neutral mechanism for serializing structured data. Proto3 is the current version used for gRPC service definitions.

**Official Docs:** https://protobuf.dev/  
**Format:** `.proto` files  
**Use Case:** gRPC APIs, efficient binary serialization

---

## Why Protocol Buffers

**Benefits:**
- Strongly typed contracts
- Efficient binary serialization (smaller than JSON)
- Backwards and forwards compatibility
- Auto-generate code for multiple languages
- Built-in versioning via field numbers
- Optimized for gRPC

---

## Basic Structure

```protobuf
syntax = "proto3";

package taxmanagement.v1;

option go_package = "github.com/example/tms/pb/v1";

// Service definition
service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}

// Messages (data structures)
message GetUserRequest {
  string user_id = 1;
}

message GetUserResponse {
  User user = 1;
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  Role role = 4;
}

enum Role {
  ROLE_UNSPECIFIED = 0;
  ROLE_USER = 1;
  ROLE_ADMIN = 2;
}
```

---

## Syntax Declaration

```protobuf
// Always use proto3 (not proto2)
syntax = "proto3";
```

---

## Package

```protobuf
// Package name (namespace)
package taxmanagement.v1;

// Language-specific options
option go_package = "github.com/example/tms/pb/v1";
option java_package = "com.example.tms.v1";
option java_outer_classname = "TaxManagementProto";
option csharp_namespace = "TaxManagement.V1";
```

---

## Scalar Types

```protobuf
message Example {
  // Double (64-bit float)
  double price = 1;
  
  // Float (32-bit float)
  float percentage = 2;
  
  // Int32 (32-bit signed integer)
  int32 count = 3;
  
  // Int64 (64-bit signed integer)
  int64 large_number = 4;
  
  // Uint32 (32-bit unsigned integer)
  uint32 positive_count = 5;
  
  // Uint64 (64-bit unsigned integer)
  uint64 large_positive = 6;
  
  // Bool
  bool is_active = 7;
  
  // String (UTF-8 or 7-bit ASCII)
  string name = 8;
  
  // Bytes (arbitrary byte array)
  bytes data = 9;
}
```

**Type Mapping:**

| Proto3 | Go | Java | Python | C++ |
|--------|----|----|--------|------|
| double | float64 | double | float | double |
| float | float32 | float | float | float |
| int32 | int32 | int | int | int32 |
| int64 | int64 | long | int | int64 |
| uint32 | uint32 | int | int | uint32 |
| uint64 | uint64 | long | int | uint64 |
| bool | bool | boolean | bool | bool |
| string | string | String | str | string |
| bytes | []byte | ByteString | bytes | string |

---

## Messages

```protobuf
message User {
  // Field number (unique, never reuse)
  string id = 1;
  string email = 2;
  string name = 3;
  Role role = 4;
  
  // Nested message
  Profile profile = 5;
  
  // Repeated field (array)
  repeated string tags = 6;
  
  // Map
  map<string, string> metadata = 7;
  
  // Timestamp (well-known type)
  google.protobuf.Timestamp created_at = 8;
  
  // Optional (explicit null handling)
  optional string phone = 9;
}

message Profile {
  string bio = 1;
  string avatar_url = 2;
}
```

---

## Enums

```protobuf
enum Role {
  // First value must be 0
  ROLE_UNSPECIFIED = 0;
  ROLE_USER = 1;
  ROLE_ADMIN = 2;
  ROLE_SYSTEM_ADMIN = 3;
}

enum Status {
  STATUS_UNSPECIFIED = 0;
  STATUS_ACTIVE = 1;
  STATUS_INACTIVE = 2;
  STATUS_PENDING = 3;
}

message User {
  Role role = 1;
  Status status = 2;
}
```

**Best Practice:** Always use `ENUM_NAME_UNSPECIFIED = 0` as default.

---

## Repeated Fields (Arrays/Lists)

```protobuf
message ListUsersResponse {
  // List of users
  repeated User users = 1;
  
  // List of strings
  repeated string tags = 2;
  
  // List of integers
  repeated int32 scores = 3;
}
```

---

## Maps

```protobuf
message User {
  // Map<string, string>
  map<string, string> metadata = 1;
  
  // Map<string, int32>
  map<string, int32> scores = 2;
  
  // Map<string, Message>
  map<string, Profile> profiles = 3;
}
```

**Note:** Map keys can be any scalar type except float/double/bytes.

---

## Well-Known Types

```protobuf
import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";
import "google/protobuf/empty.proto";
import "google/protobuf/wrappers.proto";

message Example {
  // Timestamp (date-time)
  google.protobuf.Timestamp created_at = 1;
  
  // Duration (time span)
  google.protobuf.Duration timeout = 2;
  
  // Empty (no data)
  google.protobuf.Empty empty = 3;
  
  // Nullable string
  google.protobuf.StringValue optional_string = 4;
  
  // Nullable int32
  google.protobuf.Int32Value optional_int = 5;
  
  // Nullable bool
  google.protobuf.BoolValue optional_bool = 6;
}
```

---

## Services (gRPC)

### Unary RPC (Request-Response)

```protobuf
service UserService {
  // Single request, single response
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
}

message GetUserRequest {
  string user_id = 1;
}

message GetUserResponse {
  User user = 1;
}
```

### Server Streaming

```protobuf
service UserService {
  // Single request, stream of responses
  rpc ListUsers(ListUsersRequest) returns (stream User);
}

message ListUsersRequest {
  int32 page_size = 1;
}
```

### Client Streaming

```protobuf
service UserService {
  // Stream of requests, single response
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse);
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
}

message CreateUsersResponse {
  int32 users_created = 1;
}
```

### Bidirectional Streaming

```protobuf
service ChatService {
  // Stream of requests, stream of responses
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

message ChatMessage {
  string user_id = 1;
  string text = 2;
  google.protobuf.Timestamp timestamp = 3;
}
```

---

## Complete Service Example

```protobuf
syntax = "proto3";

package taxmanagement.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

option go_package = "github.com/example/tms/pb/v1";

// User service
service UserService {
  // Get single user by ID
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  
  // List users with pagination
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  
  // Create new user
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  
  // Update existing user
  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
  
  // Delete user
  rpc DeleteUser(DeleteUserRequest) returns (google.protobuf.Empty);
  
  // Stream user updates
  rpc WatchUsers(WatchUsersRequest) returns (stream User);
}

// Tax calculation service
service TaxService {
  rpc CalculateTax(CalculateTaxRequest) returns (CalculateTaxResponse);
  rpc GetCalculation(GetCalculationRequest) returns (GetCalculationResponse);
}

// Messages
message GetUserRequest {
  string user_id = 1;
}

message GetUserResponse {
  User user = 1;
}

message ListUsersRequest {
  int32 page = 1;
  int32 page_size = 2;
  Role role_filter = 3;
}

message ListUsersResponse {
  repeated User users = 1;
  int32 total_count = 2;
  int32 page = 3;
  int32 total_pages = 4;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
  Role role = 3;
}

message CreateUserResponse {
  User user = 1;
}

message UpdateUserRequest {
  string user_id = 1;
  optional string email = 2;
  optional string name = 3;
  optional Role role = 4;
}

message UpdateUserResponse {
  User user = 1;
}

message DeleteUserRequest {
  string user_id = 1;
}

message WatchUsersRequest {
  Role role_filter = 1;
}

message CalculateTaxRequest {
  string user_id = 1;
  double gross_salary = 2;
  double allowances = 3;
  double deductions = 4;
}

message CalculateTaxResponse {
  Calculation calculation = 1;
}

message GetCalculationRequest {
  string calculation_id = 1;
}

message GetCalculationResponse {
  Calculation calculation = 1;
}

// Data models
message User {
  string id = 1;
  string email = 2;
  string name = 3;
  Role role = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
}

message Calculation {
  string id = 1;
  string user_id = 2;
  double gross_salary = 3;
  double tax_amount = 4;
  double effective_rate = 5;
  CalculationStatus status = 6;
  google.protobuf.Timestamp created_at = 7;
}

enum Role {
  ROLE_UNSPECIFIED = 0;
  ROLE_USER = 1;
  ROLE_ADMIN = 2;
  ROLE_SYSTEM_ADMIN = 3;
}

enum CalculationStatus {
  CALCULATION_STATUS_UNSPECIFIED = 0;
  CALCULATION_STATUS_PENDING = 1;
  CALCULATION_STATUS_COMPLETED = 2;
  CALCULATION_STATUS_FAILED = 3;
}
```

---

## Comments

```protobuf
// Single-line comment

/*
 * Multi-line comment
 * Document your services and messages
 */

message User {
  // User's unique identifier
  string id = 1;
  
  /*
   * User's email address
   * Must be unique across all users
   */
  string email = 2;
}
```

---

## Field Numbers

**Rules:**
- Must be unique within message
- Range: 1 to 536,870,911
- Reserved: 19,000 to 19,999 (internal use)
- **Never reuse** field numbers (breaks compatibility)
- 1-15: Most efficient encoding (use for frequent fields)
- 16+: Larger encoding

```protobuf
message User {
  string id = 1;        // Efficient
  string email = 2;     // Efficient
  string name = 3;      // Efficient
  repeated string tags = 100;  // Less efficient
}
```

---

## Reserved Fields

```protobuf
message User {
  // Reserve deleted field numbers
  reserved 5, 8 to 15;
  
  // Reserve deleted field names
  reserved "old_field", "deprecated_field";
  
  string id = 1;
  string email = 2;
  string name = 3;
  // Field 5 was deleted (reserved)
}
```

---

## Imports

```protobuf
import "google/protobuf/timestamp.proto";
import "taxmanagement/v1/common.proto";

message User {
  google.protobuf.Timestamp created_at = 1;
  common.Address address = 2;
}
```

---

## Code Generation

### Generate for Go

```bash
# Install protoc
# Download from https://github.com/protocolbuffers/protobuf/releases

# Install Go plugin
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Generate code
protoc --go_out=. --go_opt=paths=source_relative \
  --go-grpc_out=. --go-grpc_opt=paths=source_relative \
  user.proto
```

### Generate for Python

```bash
# Install plugin
pip install grpcio-tools

# Generate code
python -m grpc_tools.protoc -I. \
  --python_out=. \
  --grpc_python_out=. \
  user.proto
```

### Generate for Java

```bash
# Using Maven plugin
<plugin>
  <groupId>org.xolstice.maven.plugins</groupId>
  <artifactId>protobuf-maven-plugin</artifactId>
  <configuration>
    <protocArtifact>com.google.protobuf:protoc:3.21.7:exe:${os.detected.classifier}</protocArtifact>
  </configuration>
</plugin>
```

---

## Validation

```bash
# Validate proto file
protoc --proto_path=. \
  --descriptor_set_out=/dev/null \
  user.proto

# If valid, no output
# If invalid, shows errors
```

---

## Best Practices

1. **Always use proto3** (not proto2)
2. **Never reuse field numbers**
3. **Use enums starting with 0_UNSPECIFIED**
4. **Reserve deleted fields**
5. **Use snake_case for fields** (id_number not idNumber)
6. **Use PascalCase for messages** (UserProfile not user_profile)
7. **Package names lowercase** (taxmanagement.v1)
8. **Version your packages** (v1, v2)
9. **Import well-known types** for timestamps, durations
10. **Document with comments**

---

## Common Patterns

### Pagination

```protobuf
message ListRequest {
  int32 page = 1;
  int32 page_size = 2;
}

message ListResponse {
  repeated Item items = 1;
  int32 total_count = 2;
  int32 page = 3;
  int32 total_pages = 4;
}
```

### Error Handling

```protobuf
message Response {
  oneof result {
    Success success = 1;
    Error error = 2;
  }
}

message Success {
  User user = 1;
}

message Error {
  string code = 1;
  string message = 2;
  map<string, string> details = 3;
}
```

---

## Resources

- **Protobuf Docs:** https://protobuf.dev/
- **Language Guide:** https://protobuf.dev/programming-guides/proto3/
- **gRPC:** https://grpc.io/
- **Buf (Modern Protobuf Tool):** https://buf.build/

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial Protocol Buffers (proto3) quick reference
- Covers service definitions, messages, types, streaming
